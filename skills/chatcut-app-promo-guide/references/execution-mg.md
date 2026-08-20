# 执行路径：MG 动画

用 Motion Graphics 分段生成视频的完整执行指南。

## 品牌注入

每个 MG 的 authored design 必须包含 Phase 1 提取的品牌参数，让成品与产品网站视觉一致：

- **颜色**：primary、accent、background、text 色值（从 `branding.colors`）
- **字体**：font family（从 `branding.typography.fontFamilies`）
- **圆角**：borderRadius（从 `branding.spacing`）
- **按钮/CTA 样式**：如 MG 中有按钮，用 `branding.components` 的样式

内置 ChatCut Agent 将这些值写进 `motion-graphic-gen` 的生成 brief，并通过 `designStyle: "core"` 注入当前项目 Design Style；ACP/local CLI 则把它们作为 `create-motion-graphics` 的设计约束和可编辑 properties。不要只把品牌信息留在聊天文本里。

## MG 创作要求

**Skill**：内置 ChatCut Agent 使用 `motion-graphic-gen`；ACP/local CLI 使用 `create-motion-graphics`

- 功能展示 MG → 必须使用提取的原始图片
- Logo 动画 → 必须使用提取的真实 Logo
- 内置 ChatCut Agent 通过 `submit_motion_graphic` 生成可编辑 MG，并按该 Skill 的视觉对齐、Design Style 读取和验证流程执行；为每段 MG 编写完整 generation brief，完成后用 `track_progress` 获取资产，再放入时间线。
- ACP/local CLI 通过 `create_motion_graphic_from_code` 直接创作可编辑 JSX，不调用 `submit_motion_graphic`，再按 direct-authoring Skill 的流程放入时间线并验证。

---

## 模式 A：TTS 旁白流程（默认）

**流程**：TTS 生成 → 视觉匹配 TTS → 背景音乐 → 时间线编排

### A.1 TTS 生成

**Skill**：`voice`

1. 按脚本分段写文案（Hook / Solution / Features / CTA）
2. 分段或分句生成 TTS，方便与画面匹配
3. 获取各段时间戳，规划视觉

**质感要求**：高级专业、语速适中、有呼吸感。语言匹配：中文产品 → 中文旁白，英文产品 → 英文旁白。

### A.2 视觉生成

根据分镜规划，为每个段落生成 MG：

- TTS 是内容主导，画面跟着 TTS 走
- 根据 TTS 时间戳精确规划每段 MG 的时长
- 语义配合：画面内容与当前旁白语义相关
- TTS 不必贯穿全片，可以有呼吸感

### A.3 背景音乐

**Skill**：`music`

音量 0.2-0.3（旁白为主，音乐为辅），风格与产品调性一致，开头渐入结尾渐出。

### A.4 时间线编排

**Tools**：`edit_item` / `edit_track` / `manage_timelines`

MG 视觉放在可用视频轨；旁白和音乐放在独立音轨，避免覆盖或混在同一条音频轨上。

- MG 内容变化与 TTS 语义对应
- 片段之间快速淡入淡出（0.1-0.2s）
- 精确文字（功能名、CTA、网址）后期叠加

---

## 模式 B：纯音乐卡点流程

**流程**：音乐生成 → 选段 → 节拍分析 → 筛选关键卡点 → MG 生成 → 时间线编排

### B.1 音乐生成与选段

**Skill**：`music`

选段标准：节奏明显有起伏、有明显重拍和节奏点。音量保持原始（无旁白）。

### B.2 节拍分析

```python
import librosa
y, sr = librosa.load('music.mp3')
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)
```

### B.3 筛选关键卡点

不需要每个节拍都卡，筛选 8-10 个最重要的点：开头（第一个视觉冲击）/ 段落转折 / 高潮 / 结尾（CTA）。

### B.4 MG 创作

创作 MG 时把 BPM 和关键节拍时间落实到组件内部 timing，让动画卡上节拍。

### B.5 时间线编排

Use the same track-gravity layout rule above: MG-only visuals collapse to V1, and music-only audio collapses to A1.

MG 起点精确对齐关键卡点时间。

---

## 参考案例

### SaaS 效率工具 · 15s · TTS 旁白

**产品**：项目管理工具 | 品牌色：深蓝 + 白

```text
参考图：
- @图片1：App Logo
- @图片2：Dashboard 主界面截图
- @图片3：看板视图截图
- @图片4：分析报表截图

旁白："Still drowning in sticky notes and scattered tasks? Meet ProjectFlow. One clean dashboard for everything. Drag, drop, done. Track your team's progress in real time. Ship faster, stress less. Start free today."

(0-3s) MG：Show text: 'Sticky notes? Scattered tasks?' Brand: #1E3A5F primary, #FFFFFF text.
(3-5s) MG：Show @图片1 logo. Brand: #1E3A5F bg, #FFFFFF text.
(5-9s) MG：Show @图片2 dashboard screenshot. Text: 'One dashboard for everything.'
(9-12s) MG：Show @图片3 kanban screenshot. Text: 'Drag, drop, done.'
(12-15s) MG：Show @图片4 analytics screenshot + logo. Text: 'Start Free', URL 'projectflow.com'.
```

**套路**：痛点 Hook 用文字 MG，中间段用截图 + 文字叠加，CTA 收尾，全程统一品牌色，并保留用户会修改的内容与品牌字段为 properties。

### 创意设计工具 · 15s · 纯视觉冲击

**产品**：AI 设计工具 | 品牌色：紫 + 渐变

```text
参考图：
- @图片1：App Logo
- @图片2：用户作品 1
- @图片3：用户作品 2
- @图片4：编辑器界面截图

旁白："Design without limits. One prompt, infinite possibilities. From concept to creation in seconds. This is DesignAI."

(0-3s) MG：Show @图片1 logo. Brand: #7C3AED primary, #E9D5FF accent.
(3-6s) MG：Show @图片2. Text: 'One prompt, infinite possibilities.'
(6-9s) MG：Show @图片3. Text: 'From concept to creation.'
(9-12s) MG：Show @图片4 editor screenshot. Text: 'Design without limits.'
(12-15s) MG：Show logo. Text: 'DesignAI', CTA 'Try Free'. Brand: #7C3AED primary.
```

**套路**：用户作品做素材，极简旁白，每 3s 一个大视觉变化，用同一套 authored visual system 保持一致。
