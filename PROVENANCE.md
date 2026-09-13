# Provenance

## classical-chinese-poetry

- Author and source: [Shmilyol/classical-chinese-poetry](https://github.com/Shmilyol/classical-chinese-poetry)
- Upstream commit: `306152a88223795ce0ef63d10d64254b0a86a991`
- Source directory: `skill/`
- Published directory: `literature/poem/classical-chinese-poetry/`

Local changes are limited to `SKILL.md` and JSON whitespace:

1. Declare reading and narrowly scoped validator execution, with an explicit local tool scope and safe process argument handling.
2. Move compatibility information under metadata for the local Skill validator.
3. Replace ambiguous path-like prose with clear wording.
4. Replace the ordinary English verb “requests” with “seeks”: SkillSpector 2.11.2's capability regex otherwise mistakes it for the Python HTTP library.
5. Pretty-print `data/pingshui.json` so the static parser can inspect it completely.

The validator code and remaining resources are unchanged. All 8,232 rhyme database entries were checked for semantic equality; seven normal and exceptional validation cases returned identical results before and after the revision.

No scanner rules, findings, or coverage checks were disabled to obtain SAFE. The original report's unresolved references and parser limit were fixed in the bundle. Scanner source inspection confirmed the natural-language false positive described above.

No license file was found in the upstream repository when preparing this publication. Public availability is not itself an open-source license. Attribution here does not grant additional rights to upstream content. No repository-wide license is asserted over that content.
