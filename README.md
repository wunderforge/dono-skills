# Dono's Skills

[![SkillSpector](https://github.com/wunderforge/dono-skills/actions/workflows/skillspector.yml/badge.svg)](https://github.com/wunderforge/dono-skills/actions/workflows/skillspector.yml)

A categorized collection of agent skills for Chinese poetry and video direction.

## 目录 / Catalog

```text
literature/
└── poem/
    └── classical-chinese-poetry/
        ├── SKILL.md
        ├── data/pingshui.json
        ├── scripts/validate_poem.py
        ├── references/
        └── examples/

media/
└── video/
    └── ogilvideo-local/
        ├── SKILL.md
        ├── LICENSE
        └── references/project-direction.md
```

| 分类 | Skill | 能力 |
| --- | --- | --- |
| literature / poem | [classical-chinese-poetry](literature/poem/classical-chinese-poetry/SKILL.md) | 写作、修改、评析五绝、七绝、五律、七律；平水韵与平仄辅助检查 |
| media / video | [ogilvideo-local](media/video/ogilvideo-local/SKILL.md) | 创业大赛 60 秒开场 pitch 导演：叙事、旁白、逐镜头时间线、即梦提示词与审片；含 BN 热界面膜项目参考 |

The exact installable directory is [literature/poem/classical-chinese-poetry](https://github.com/wunderforge/dono-skills/tree/main/literature/poem/classical-chinese-poetry).
Use that URL with an Agent Skills installer such as agent-capability-lab.

Example: `用 classical-chinese-poetry 写一首七绝：秋夜湖边，怀念故友，含蓄温暖。`

Python 3 enables the bundled validator. No third-party Python packages are needed for poetry validation. The skill also supports reference-based checks without Python. Modern poetry, lyrics and ci forms are outside this skill's scope; ambiguous readings and literary quality still require judgment.

### Video direction

The exact installable directory is [media/video/ogilvideo-local](https://github.com/wunderforge/dono-skills/tree/main/media/video/ogilvideo-local).

Example: `用 ogilvideo-local 为创业大赛设计 60 秒开场 pitch，给出旁白、逐镜头表、即梦提示词和素材缺口，结尾衔接现场路演。`

This is a written direction workflow adapted from Ogilvideo, with no bundled executable scripts or required API credentials. Media generation and inspection use the tools available to the agent. The BN film reference is a project brief, not independently verified evidence; replace its product facts and audience when adapting it to another project. The upstream MIT license is retained in the skill directory.

## Security checks

Every push and pull request runs `.github/workflows/skillspector.yml`; manual runs are also available.
The workflow discovers every `SKILL.md` directory and scans the entire bundle with NVIDIA SkillSpector **2.11.2**, pinned to commit `1c0eb569a2550172415aaebd83a62ea163cb3c06`.

The gate uses the same criteria as agent-capability-lab: successful execution, complete analysis, 100% coverage, a SAFE recommendation, no HIGH or CRITICAL findings, and completed supply-chain, prompt-injection and data-exfiltration analyzers. Scanner errors fail the job. JSON reports are retained as workflow artifacts, including failed runs. Tests exercise the gate against incomplete and unsafe reports.

This is static scanning (`--no-llm`); LLM semantic analyzers are not enabled and no API keys are required. A passing scan is evidence for the scanned revision, not a guarantee of safety. Publishing a later revision triggers a fresh scan.

To reproduce in an isolated Python 3.12 environment:

```sh
python -m pip install -r requirements-scan.txt
python -m unittest discover -s tests -v
python scripts/scan_skills.py
```

## 来源与修改 / Provenance

See [PROVENANCE.md](PROVENANCE.md) for the upstream author, exact source revision and local changes. Third-party material retains its original rights; this repository does not assign it a new license.
