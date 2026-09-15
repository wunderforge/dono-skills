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

## ogilvideo-local

- Author and source: [BuilderStudio / wundercorp/ogilvideo-skill](https://github.com/wundercorp/ogilvideo-skill).
- Upstream commit: `8d2480a339798a012cf3799044577d00195e2748`.
- Source file: `skills/ogilvideo/SKILL.md`.
- Published directory: `media/video/ogilvideo-local/`.
- Upstream MIT permission notice and copyright are retained verbatim in the skill's `LICENSE`.

Adaptations:

1. Rename the skill to `ogilvideo-local` and focus discovery on startup competition opening videos.
2. Replace two ambiguous slash-separated phrases with ordinary prose: “before-and-after contrast” and a comma-separated list of animation tools. SkillSpector 2.11.2 interpreted the original phrases as unresolved local references; inspection of the pinned source confirmed that they were prose, not file reads.
3. Add a local scope section that keeps work within the user's request, allows production roles to be handled sequentially, and distinguishes actual media review from historical proposals.
4. Add a self-contained BN Thermal Highway brief covering the audience, three-layer product geometry, evidence boundaries, shot prompts, sound, and handoff to a live pitch. This reference preserves project assumptions and explicitly requires evidence for factual claims.
5. Remove the dependency on a particular local project directory. No original helper scripts, Git hooks, accounts, or API credentials are included.

The earlier project-local installation was explicitly user-authorized after the upstream scan was incomplete. Publication is a separate step and uses this repository's unchanged complete-SAFE gate. No scanner rules or checks are disabled for this adaptation. Scan reports are generated under the ignored `reports` directory and retained by CI as artifacts.

Pre-publication validation on 2026-09-15: SkillSpector 2.11.2 returned SAFE with complete analysis, 100% coverage of all 3 components, zero issues, and zero unresolved references. The skill format validator and the repository's three security-gate tests also passed. This is static analysis without LLM semantic analyzers. The scanned entrypoint SHA-256 is `6ed322aed771b1d6d8d077d13ad5843feda2989239b49c3cd173abae78dba7fa`.
