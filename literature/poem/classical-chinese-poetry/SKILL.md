---
name: classical-chinese-poetry
allowed-tools: Read Bash(python scripts/validate_poem.py:*)
description: >
  Create, revise, validate, and critique traditional Chinese regulated verse
  (五言绝句、七言绝句、五言律诗、七言律诗).
  Use when the user asks to 写诗、作诗、改诗、评诗、检查格律、
  检查押韵、炼字、润色古诗, or seeks classical Chinese poetry
  composition, revision, or prosody checking.
metadata:
  compatibility: >
    Core workflow requires only Skill resource reading.
    Python 3 enables optional deterministic prosody validation
    using the bundled validator and Pingshui rhyme database.
---

# Classical Chinese Poetry Craft

Plan · Compose · Validate · Critique · Revise

## Local tool scope

Read only this skill's bundled resources and poem text supplied by the user.
Optional execution is limited to `scripts/validate_poem.py` with poem text and form
passed as separate process arguments, never interpolated into shell code. Run from
the skill directory. The validator reads `data/pingshui.json` and prints its report;
it needs no network access, package installation, or file writes. Tool declarations
describe this scope; the host remains responsible for enforcing permissions.

v0.1 只做近体诗：五绝、七绝、五律、七律。韵书只用平水韵。统一简体。

## 何时不用

现代诗、歌词、普通中文文案、诗词事实问答、独立翻译任务。这些不要加载本 Skill 的创作流程。写诗输出中的【译文】是注释，不是独立翻译。

## 模型能力

本 Skill 放大已有的古典文学能力，不能从零制造它。弱模型优先 Quick；对平仄不要假装确定，标「此处格律判断存在不确定性」。

## Workflow

1. Interpret
2. Plan
3. Compose（只写 1 首）
4. Check（Python validator 或本文件 + `references/meter.md`）
5. Critique
6. 合并 issues，按 fatal > major > quality 排序
7. 只修最高优先级 1–2 项（constraint lock）
8. Recheck，最多 3 轮
9. Output

## 模式

| 模式 | 何时 | 检查 | 改稿 | 输出 |
|------|------|------|------|------|
| Quick | 用户要快、不在意格律 | 一次硬检查 | 0 | 诗作 |
| Standard | 默认 | 完整 | ≤3 | 诗作 + 译文 + 注释 + 出处 |
| Master | 用户要看过程 | 完整 | ≤3 | 规划 + 检查 + 修改记录 + 定稿 + 译文 + 注释 + 出处 |

---

## 1. Interpret

从用户话里抽出，缺省则自定并在心里记住（Master 要写出来）：

- form: `wujue` / `qijue` / `wulv` / `qilv`
- theme, scene, emotion
- style: 盛唐明快型 / 中晚唐沉郁型 / 用户指定
- imagery: 指定意象
- mode: quick / standard / master
- 核心情感：当用户给的是散文、现代诗或一段话，用一句话概括其情感核心。必须保住原文的温度关系（如「得你一枝」里的「你」），不要收成纯风景。后续 Plan 围绕这个核心展开，不逐句翻译原文。
- 若用户给的是成诗 + 改/查：进入改诗路径，跳过 Compose，从 Check 开始

## 2. Plan

读 `references/imagery.md`。Quick 只写一句结构概要。

Standard / Master 在逐句规划前，先定：

1. **统一场景**：选一个具体可感的空间/时间（如「雨后驿路骑马」「秋夜湖岸」），四句都在里面。
2. **镜头编排**：起=远景/环境，承=推近，转=情感拐点，合=停在一个带电的点上。
3. **转合落点**：转、合两句要负责把核心情感送进去。落点必须可感（动作、问句、被情浸透的物），不要抽象判断（「春已换」「不必叹」）。合句读完应有余味，不能只是再拍一张风景。

当用户原文有多层意思时，不要逐层对应每一句。允许省略、合并、用画面暗示。四句读完，没看过原文的人也应隐约感到那个核心情感。

然后为每句写：

- 功能：起 / 承 / 转 / 合（律诗后四句再走一轮起承转合或前写景后抒情）
- 主意象
- 情绪
- 画面自检：这句能画成画吗？如果主意象是抽象概念而非可感物件或动作，换掉。

标注风险意象（季节/空间张力），不要写成「禁用」。

## 3. Compose

读 `references/styles.md`。只生成 1 首。不要手机、地铁、焦虑值等现代词；现代题材须古典化。不要堆「岁月悠悠 / 独倚高楼 / 一轮明月 / 清风徐来」。

寓情于景，不直接说理。起句和承句必须包含具体可感的画面或动作（能画成画的）。

转合负责抒情，但要用带电的画面，不要旁白。转句让人看见拐点（驻足、花已别样），不要下结论（「春已换」）。合句把核心情感落到一个点上（拈花、袖底留香、襟上未干），停住，留余味。不写「不必」「何须」「休叹」等纯理性判断词开头的句子。自检：把后两句单独念给没看过原文的人，他若只感到「风景挺美」而感觉不到核心情感，重写转合。

意象密度：绝句核心意象（名词性画面元素）不超过 5–6 个。只出现一次且不被其他句呼应的意象，考虑去掉或替换。避免生造词组合，优先用古人已用过的搭配；自检：这个两字组合能想到古人用过的出处吗？想不到就换。

## 4. Check

统一产出 issue 列表，每条含 `priority` + 说明。

### Enhanced（能跑 Python）

```bash
python scripts/validate_poem.py --poem "句1\n句2\n..." --form qijue
```

以 YAML 为准：`fail` → issue；`unclear` → 结合句义判断，不得改标成确定 pass。

### Portable（不能跑脚本）

读 `references/meter.md`：

1. 句数、每句字数
2. 韵脚是否同一平水韵部（入声字是仄，不能当平韵）
3. 二四六字与句末是否合所选格式

不确定就标 unclear，不要编造韵部。

## 5. Critique

文学软评价，不重复已由 Check 判定的字数/韵脚（除非你认为 validator 漏了）：

- 起承转合是否连得上
- 意象季节/空间：读 `references/imagery.md`，区分无意冲突与有意反常
- 现代口语
- 律诗颔联颈联对仗（validator 只标 `requires_llm_review`）
- 套话密度：一首七绝出现 ≥2 个高频套语则记 quality
- 画面密度：起句和承句是否有具体可感意象？起承中有一句纯议论（无法画成画）则记 quality
- 场景统一：绝句四句是否共享一个可感空间？分属三个以上不同场景且无过渡则记 quality
- 意象密度：绝句核心意象超过 6 个，且有 ≥3 个「一次性意象」（只出现一次就消失）则记 quality
- 转合落点：后两句是否把核心情感落到可感的点上？若只是继续报风景，或出现「已换 / 不必 / 何须」这类判断而无画面，记 quality
- 余味：合句读完是否停得住？若只是动作交代（「花入衣襟」）而无陪伴/释然等温度，记 quality

## 6–7. Fix

优先级：

```yaml
fatal:
  - 字数 / 句数错误
  - 明确押错韵
major:
  - 关键位置严重失律
  - 律诗必要联明显不成对仗
  - 明显现代口语
quality:
  - 章法、意象、套话、炼字
```

每轮只改 1–2 个最高项。**Constraint lock：** 修低优先级时不得破坏已通过的更高项（字数、已通过韵脚、用户指定意象与主题）。

## 8. Recheck

改完回到 Check。最多 3 轮。

3 轮后仍有 fatal 或 major：输出当前最佳稿 + 未解决 issues，明确告诉用户哪几处不合律。禁止假装成功。

## 9. Output

注释是终稿确定后的后处理，不参与 Check / Fix 循环。不要把内部 YAML 倒给用户，除非对方要看检查。

### 输出结构

Quick：诗题（可自拟）+ 正文。

Standard / Master：

```
诗题
正文

【译文】
【注释】
【词句出处】
```

Master 额外在正文前展示：创作规划 → 初稿 → 检查要点 → 修改记录。展示可验证中间产物，不要展示思维链。

### 译文

散文型译文：本身也是一段美文。准确是底线，同时要传递原诗的情绪温度。

1. **全词白话化**：凡现代口语中不常用的词，必须换为白话。判定：如果这个词需要出现在【注释】里，那它在译文中不该保留原样。例：「案头」→「书桌上」，不可写成「案头的秋日影子」。
2. **逐句对应**：不遗漏任何一句。
3. **不歪曲**：不添加原诗没有的实体（人物、地点、事件、物件）。
4. **还原感官**：古诗七字压缩了画面，译文应将省略的感官细节还原（视觉、听觉、嗅觉、触觉、动作），只要原诗语境隐含了它。「味转赊」→「茶味在舌尖慢慢散开」；「盈襟」→「落进衣襟里」。
5. **保留文气**：译文读起来像散文，不像说明书。情绪温度跟原诗对齐；长短句交错；可适度拟人或比喻，只要原诗意境隐含了。

刹车规则：译文中每个名词和动词，原诗中必须有对应意象或动作。找不到对应 → 删掉。

生成后自检：注释里出现的词，译文中必须已换成白话；译文中不得出现原诗没有的实体。

### 注释

只选三类词：生僻字词（现代人不认识或不知古义）、特殊语境义（常见字取非常见义）、古典化改写（古典表达包装的现代概念）。

格式：`- **词**：释义。补充说明（可选）。`

不注释现代人能看懂的词。每句选 0–2 个词。一条 1–2 句，不写论文。

### 词句出处

指出用词 / 意象在古人名作中的先例。分两类：

- **词汇级**：同一个词在名诗中出现。直接引用原文。
- **意境级**：手法 / 意象相类。用「意近」「手法相类」限定。

诚实原则：只引确信存在的名句；不确定原文是否逐字准确 → 用「意近」，不加引号伪装；绝不编造「诗人 + 诗题 + 诗句」的完整组合；每首诗 2–4 处，不贪多。

### 不同任务

| 任务 | 译文 | 注释 | 出处 |
|------|------|------|------|
| 写诗 | ✅ | ✅ | ✅ |
| 改诗 | ✅（改后版本） | ✅ | ✅ |
| 评诗 | ❌ | ✅ | ✅ |
| 查格律 | ❌ | ❌ | ❌ |

用户说「不要注释」「只要诗」时可关闭。改诗只动必须动的字；用户说「只改格律」则其他句原样保留。

## 完整示例

见 `examples/master-example.md`。
