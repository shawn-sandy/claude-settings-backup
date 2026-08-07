#!/usr/bin/env python3
"""Self-contained check for vscode-settings-audit.py. Run: python3 this_file.py

Guards the classification rules that decide what --apply deletes. Every assert
here corresponds to a way the audit was observed to go wrong on real data.
"""
import glob, importlib.util, json, os, shutil, sys, tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    'audit', os.path.join(_HERE, 'vscode-settings-audit.py'))
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

LIVE = {'eslint.enable', 'gitlens.graph.layout'}
CORE = {'git.autofetch', 'npm.enableRunFromFolder'}


def c(key):
    return audit.classify(key, LIVE, CORE)


def main():
    # A key an installed extension declares is live.
    assert c('eslint.enable') == 'LIVE'

    # A key a bundled VS Code extension declares is not an orphan.
    assert c('git.autofetch') == 'BUNDLED'

    # Core product settings have no package.json anywhere; the prefix list covers them.
    assert c('editor.formatOnSave') == 'CORE'
    assert c('workbench.colorTheme') == 'CORE'

    # Nothing declares this -> prunable.
    assert c('cody.suggestions.mode') == 'ORPHAN'

    # Regression: VS Code bundles a `copilot` stub declaring github.copilot.*
    # even with the extension absent. If BUNDLED_STUBS stops filtering it, dead
    # Copilot config becomes permanently unprunable.
    assert 'copilot' in audit.BUNDLED_STUBS
    assert 'github.copilot.enable' not in audit.bundled_keys(), \
        'bundled copilot stub is leaking github.copilot.* into the keep-set'
    assert c('github.copilot.enable') == 'ORPHAN'

    # Regression: an installed extension that no longer declares a key means the
    # key is deprecated, not protected. GitLens is installed; this key is dead.
    assert c('gitlens.experimental.generateCommitMessagePrompt') == 'ORPHAN'

    # Regression: user dictionaries outlive their extension and must never be swept.
    assert c('cSpell.userWords') == 'USERDATA'

    # Language blocks route to the dangling-formatter pass, never to orphan pruning.
    assert c('[markdown]') == 'LANG'
    assert c('[typescriptreact]') == 'LANG'

    # Regression: prefix matching must not treat a hyphenated sibling as covered.
    # 'github.copilot' + '.' does not match 'github.copilot-labs.*'.
    assert c('github.copilot-labs.showBrushesLenses') == 'ORPHAN'

    # A [lang] block only applies if something registers that language id.
    # '[nunjucks]' sat in settings for months formatting nothing.
    keys = ['[mdx]', '[nunjucks]', '[css]', 'editor.formatOnSave']
    assert audit.dead_language_blocks(keys, {'mdx', 'css'}) == ['[nunjucks]']

    # Regression: a dead block must never be pruned -- it still carries intent
    # for whenever the language extension gets installed. LANG, not ORPHAN.
    assert c('[nunjucks]') == 'LANG'

    # language_ids parses the shape it is given. A declaration with no id, or a
    # package.json with no languages at all, must not blow up or leak a None.
    tmp = tempfile.mkdtemp()
    try:
        for name, body in (
            ('good', {'contributes': {'languages': [{'id': 'mdx'}, {'no': 'id'}]}}),
            ('none', {'contributes': {'configuration': {'properties': {}}}}),
            ('junk', None),  # written as invalid JSON below
        ):
            os.makedirs(os.path.join(tmp, name))
            p = os.path.join(tmp, name, 'package.json')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write('{not json' if body is None else json.dumps(body))
        found = audit.language_ids(glob.glob(os.path.join(tmp, '*', 'package.json')))
        assert found == {'mdx'}, f'expected exactly mdx, got {found!r}'
    finally:
        shutil.rmtree(tmp)

    # Bundled language discovery works at all -- if language_ids ever returns
    # nothing, every [lang] block in settings reads as dead and the report is
    # noise. 'markdown' is bundled; 'mdx' only ever comes from a marketplace
    # extension, so its absence proves BUNDLED points where it should.
    #
    # Note: BUNDLED_STUBS is currently a no-op for languages -- the copilot stub
    # declares only 'ignore' and 'markdown', both declared elsewhere too. The
    # filter stays for symmetry with bundled_keys, where it does matter.
    bundled = audit.bundled_languages()
    assert 'markdown' in bundled, 'bundled language discovery returned nothing useful'
    assert 'mdx' not in bundled, 'BUNDLED is resolving to the wrong extensions dir'

    print(f'ok - {main.__doc__ or "all classification checks passed"}')


main.__doc__ = 'all classification checks passed'

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print(f'FAIL: {e}', file=sys.stderr)
        sys.exit(1)
