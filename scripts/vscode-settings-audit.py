#!/usr/bin/env python3
"""Find and optionally prune orphaned keys in a VS Code settings.json.

A key is ORPHAN when no extension installed in the target profile contributes
it, no VS Code bundled extension contributes it, and it is not a core product
setting. Reports by default; --apply writes (after a timestamped backup).

    vscode-settings-audit.py                 # audit the default profile
    vscode-settings-audit.py Work            # audit a named profile
    vscode-settings-audit.py Work --apply    # ...and prune it

Settings ownership is read from each extension's contributes.configuration,
so there is no hand-maintained namespace map to drift.
"""
import json, os, re, subprocess, sys, shutil, glob, datetime

USER = os.path.expanduser('~/Library/Application Support/Code/User')
EXT_DIR = os.path.expanduser('~/.vscode/extensions')
BUNDLED = '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions'

# ponytail: core product settings are compiled into VS Code, not into any
# package.json, so this prefix list is the one thing still hand-maintained.
# A missing prefix shows up as a false ORPHAN in the report, never as a silent
# deletion -- the report is the review step. Add prefixes as they surface.
CORE_PREFIXES = (
    'editor.', 'workbench.', 'files.', 'window.', 'terminal.', 'search.',
    'debug.', 'extensions.', 'security.', 'diffEditor.', 'multiDiffEditor.',
    'scm.', 'chat.', 'notebook.', 'accessibility.', 'explorer.', 'outline.',
    'problems.', 'task.', 'telemetry.', 'update.', 'zenMode.', 'breadcrumbs.',
    'comments.', 'screencastMode.', 'keyboard.', 'application.', 'remote.',
    'mcp.', 'inlineChat.', 'interactiveWindow.', 'testing.', 'audioCues.',
    'accessibilitySignals.', 'settingsSync.', 'launch', 'merge-conflict.',
)

# Keys that are user data rather than extension config: they outlive their
# extension and must never be swept.
USER_DATA = {'cSpell.userWords', 'cSpell.words', 'cSpell.ignoreWords'}

# ponytail: VS Code bundles a `copilot` stub that declares every github.copilot.*
# setting even when the marketplace extension is absent -- trusting it whitelists
# dead Copilot config forever. Skip such stubs; add a name here if another turns up.
BUNDLED_STUBS = ('copilot',)

LANG_BLOCK = re.compile(r'^\[.+\]$')


def contributed_keys(package_json_paths):
    """Union of every settings key declared by contributes.configuration."""
    keys = set()
    for p in package_json_paths:
        try:
            with open(p, encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        conf = data.get('contributes', {}).get('configuration')
        if not conf:
            continue
        for block in ([conf] if isinstance(conf, dict) else conf):
            keys |= set(block.get('properties', {}))
    return keys


def language_ids(package_json_paths):
    """Union of every language id declared by contributes.languages."""
    ids = set()
    for p in package_json_paths:
        try:
            with open(p, encoding='utf-8') as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        for lang in data.get('contributes', {}).get('languages', []) or []:
            if lang.get('id'):
                ids.add(lang['id'])
    return ids


def dead_language_blocks(keys, langs):
    """[lang] blocks whose language id nothing registers.

    A `[foo]` block only ever applies if some extension declares `foo` as a
    language id -- otherwise the whole block is unreachable and its settings
    silently do nothing, exactly like a dangling defaultFormatter one level up.
    Reported, never pruned: an uninstalled language extension is a likely cause,
    and the block still carries the user's intent for when it is installed.
    """
    return [k for k in keys if LANG_BLOCK.match(k) and k[1:-1] not in langs]


def classify(key, live, core):
    """Verdict for one settings key. Only ORPHAN is ever pruned."""
    if LANG_BLOCK.match(key):
        return 'LANG'          # handled by the dangling-formatter pass
    if key in USER_DATA:
        return 'USERDATA'
    if key in live:
        return 'LIVE'
    if key in core:
        return 'BUNDLED'
    if key.startswith(CORE_PREFIXES):
        return 'CORE'
    return 'ORPHAN'


def _bundled_pkgs():
    return [p for p in glob.glob(os.path.join(BUNDLED, '*', 'package.json'))
            if os.path.basename(os.path.dirname(p)) not in BUNDLED_STUBS]


def bundled_keys():
    """Settings contributed by VS Code's own extensions, minus marketplace stubs."""
    return contributed_keys(_bundled_pkgs())


def bundled_languages():
    """Language ids registered by VS Code's own extensions, minus stubs."""
    return language_ids(_bundled_pkgs())


def resolve_profile(name):
    """Return (settings_path, cli_args) for a profile name."""
    if name in (None, 'default'):
        return os.path.join(USER, 'settings.json'), []
    store = os.path.join(USER, 'globalStorage', 'storage.json')
    with open(store, encoding='utf-8') as fh:
        profiles = json.load(fh).get('userDataProfiles', [])
    for p in profiles:
        if p.get('name') == name:
            loc = p['location']
            # A profile inheriting settings has no own file; it reads the global one.
            own = os.path.join(USER, 'profiles', loc, 'settings.json')
            if p.get('useDefaultFlags', {}).get('settings') or not os.path.exists(own):
                return os.path.join(USER, 'settings.json'), ['--profile', name]
            return own, ['--profile', name]
    sys.exit(f'no profile named {name!r}; found: '
             + ', '.join(sorted(p.get('name', '?') for p in profiles)))


def load_settings(path):
    """Parse settings.json. Returns (dict, is_strict_json)."""
    raw = open(path, encoding='utf-8').read()
    try:
        return json.loads(raw), True
    except ValueError:
        stripped = re.sub(r'^\s*//.*$', '', raw, flags=re.M)
        stripped = re.sub(r',(\s*[}\]])', r'\1', stripped)
        return json.loads(stripped), False


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply_changes = '--apply' in sys.argv[1:]
    profile = args[0] if args else 'default'

    path, cli = resolve_profile(profile)
    settings, strict = load_settings(path)

    installed = subprocess.run(['code'] + cli + ['--list-extensions'],
                               capture_output=True, text=True).stdout.split()
    installed_lower = {e.lower() for e in installed}

    # A profile's extensions.json can outlive the folders it points at: ids keep
    # listing while the directories are gone. Unresolved ids contribute no keys,
    # so their settings would all read as ORPHAN -- track them and refuse to write.
    ext_pkgs, unresolved = [], []
    for eid in installed_lower:
        found = glob.glob(os.path.join(EXT_DIR, eid + '-*', 'package.json'))
        ext_pkgs.extend(found) if found else unresolved.append(eid)

    live = contributed_keys(ext_pkgs)
    core = bundled_keys()
    langs = bundled_languages() | language_ids(ext_pkgs)

    dead_langs = dead_language_blocks(settings, langs)

    orphans, dangling = [], []
    for key, val in settings.items():
        verdict = classify(key, live, core)
        if verdict == 'LANG':
            # A block for a language nothing registers cannot dangle in any
            # meaningful way -- skip it so --apply never edits it.
            if key in dead_langs:
                continue
            fmt = val.get('editor.defaultFormatter') if isinstance(val, dict) else None
            if fmt and fmt.lower() not in installed_lower and not fmt.startswith('vscode.'):
                dangling.append((key, fmt))
        elif verdict == 'ORPHAN':
            orphans.append(key)

    refs = settings.get('workbench.settings.applyToAllProfiles')
    bad_refs = [r for r in refs if r not in settings] if isinstance(refs, list) else []

    print(f'profile   : {profile}')
    print(f'settings  : {path}')
    print(f'parsed as : {"strict JSON" if strict else "JSONC (comments/trailing commas)"}')
    print(f'extensions: {len(installed)} listed, {len(installed) - len(unresolved)} '
          f'resolved on disk, {len(live)} contributed keys')
    print(f'keys      : {len(settings)} total, {len(orphans)} orphaned, '
          f'{len(dead_langs)} dead [language] block(s)\n')

    if unresolved:
        print(f'!! {len(unresolved)} listed extension(s) have no folder under {EXT_DIR}.')
        print('!! Their contributed keys are invisible, so settings that belong to them')
        print('!! are misreported as ORPHAN below. Treat this report as unreliable.')
        print(f'!! e.g. {", ".join(sorted(unresolved)[:3])}\n')

    if orphans:
        print('--- ORPHANED (no installed or bundled extension contributes these) ---')
        for k in orphans:
            print(f'  {k}')
    else:
        print('--- ORPHANED: none ---')

    print('\n--- DANGLING defaultFormatter ---')
    for k, fmt in dangling or []:
        print(f'  {k} -> {fmt} (not installed)')
    if not dangling:
        print('  none')

    print('\n--- DEAD [language] blocks (no extension registers the id) ---')
    for k in dead_langs or []:
        print(f'  {k} -> install a {k[1:-1]} language extension, or drop the block')
    if not dead_langs:
        print('  none')

    print('\n--- UNRESOLVABLE applyToAllProfiles refs ---')
    for r in bad_refs or []:
        print(f'  {r}')
    if not bad_refs:
        print('  none')

    if not apply_changes:
        print('\nreport only. re-run with --apply to prune.')
        return

    if unresolved:
        sys.exit(f'\nREFUSING to rewrite: {len(unresolved)} listed extension(s) could not '
                 'be resolved on disk, so the ORPHAN list is not trustworthy.')

    if not strict:
        sys.exit('\nREFUSING to rewrite: file is JSONC and a round-trip would drop '
                 'comments. Remove them first, or prune by hand.')

    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = f'{path}.{stamp}.bak'
    shutil.copy2(path, backup)

    out = {k: v for k, v in settings.items() if k not in set(orphans)}
    for k, _ in dangling:
        block = {kk: vv for kk, vv in out[k].items() if kk != 'editor.defaultFormatter'}
        if block:
            out[k] = block
        else:
            del out[k]
    if bad_refs:
        keep = [r for r in refs if r in out]
        if keep:
            out['workbench.settings.applyToAllProfiles'] = keep
        else:
            out.pop('workbench.settings.applyToAllProfiles', None)

    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent='\t', ensure_ascii=False)
        fh.write('\n')

    print(f'\nbackup  : {backup}')
    print(f'written : {len(settings)} -> {len(out)} keys')


if __name__ == '__main__':
    main()
