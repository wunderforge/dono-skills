#!/usr/bin/env python3
"""
Classical Chinese poetry prosody validator.

Usage:
  python validate_poem.py --poem "LINE1\\nLINE2\\n..." --form qijue

Output: YAML validation report (pass / fail / unclear).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "pingshui.json"

METER_TEMPLATES = {
    "wujue": {
        "lines": 4,
        "chars": 5,
        "rhyme_positions": [2, 4],
        "parallelism_pairs": [],
        "patterns": {
            "pingqi_no_first": [
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
            ],
            "pingqi_first": [
                "平平仄仄平",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
            ],
            "zeqi_no_first": [
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
            ],
            "zeqi_first": [
                "仄仄仄平平",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
            ],
        },
    },
    "qijue": {
        "lines": 4,
        "chars": 7,
        "rhyme_positions": [2, 4],
        "parallelism_pairs": [],
        "patterns": {
            "pingqi_no_first": [
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
            ],
            "pingqi_first": [
                "平平仄仄仄平平",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
            ],
            "zeqi_no_first": [
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
            ],
            "zeqi_first": [
                "仄仄平平仄仄平",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
            ],
        },
    },
    "wulv": {
        "lines": 8,
        "chars": 5,
        "rhyme_positions": [2, 4, 6, 8],
        "parallelism_pairs": [[3, 4], [5, 6]],
        "patterns": {
            "pingqi_no_first": [
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
            ],
            "pingqi_first": [
                "平平仄仄平",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
            ],
            "zeqi_no_first": [
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
            ],
            "zeqi_first": [
                "仄仄仄平平",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
                "仄仄平平仄",
                "平平仄仄平",
                "平平平仄仄",
                "仄仄仄平平",
            ],
        },
    },
    "qilv": {
        "lines": 8,
        "chars": 7,
        "rhyme_positions": [2, 4, 6, 8],
        "parallelism_pairs": [[3, 4], [5, 6]],
        "patterns": {
            "pingqi_no_first": [
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
            ],
            "pingqi_first": [
                "平平仄仄仄平平",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
            ],
            "zeqi_no_first": [
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
            ],
            "zeqi_first": [
                "仄仄平平仄仄平",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
                "仄仄平平平仄仄",
                "平平仄仄仄平平",
                "平平仄仄平平仄",
                "仄仄平平仄仄平",
            ],
        },
    },
}

FLEXIBLE_5 = {0, 2}
FLEXIBLE_7 = {0, 2, 4}


def load_db() -> dict:
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


def normalize(raw: str) -> list[str]:
    raw = raw.replace("\\n", "\n").strip()
    chunks = re.split(r"[,，。.;；!！?？\n\r]+", raw)
    lines = []
    for chunk in chunks:
        cleaned = re.sub(r"[^\u4e00-\u9fff]", "", chunk)
        if cleaned:
            lines.append(cleaned)
    return lines


def lookup(char: str, db: dict) -> list[dict]:
    return db.get(char, [])


def tones_of(entries: list[dict]) -> set[str]:
    return {e["tone"] for e in entries}


def judge_tone(char: str, expected: str, position: int, flexible: set[int], db: dict) -> dict:
    entries = lookup(char, db)
    if not entries:
        return {
            "char": char,
            "expected": expected,
            "actual": "?",
            "status": "unclear",
            "reason": "not_in_database",
            "flexible": position in flexible,
        }

    possible = tones_of(entries)
    if possible == {expected}:
        return {
            "char": char,
            "expected": expected,
            "actual": expected,
            "status": "pass",
            "flexible": position in flexible,
        }
    if expected in possible and len(possible) > 1:
        return {
            "char": char,
            "expected": expected,
            "actual": "/".join(sorted(possible)),
            "status": "unclear",
            "reason": "multiple_readings",
            "detail": "、".join(f"{e['tone']}({e['rhyme']})" for e in entries),
            "flexible": position in flexible,
        }
    if expected not in possible:
        if position in flexible:
            return {
                "char": char,
                "expected": expected,
                "actual": "/".join(sorted(possible)),
                "status": "pass",
                "reason": "flexible_position",
                "flexible": True,
            }
        return {
            "char": char,
            "expected": expected,
            "actual": "/".join(sorted(possible)),
            "status": "fail",
            "flexible": False,
        }
    return {
        "char": char,
        "expected": expected,
        "actual": "/".join(sorted(possible)),
        "status": "pass",
        "flexible": position in flexible,
    }


def check_structure(lines: list[str], form: str, template: dict) -> dict:
    expected_lines = template["lines"]
    expected_chars = template["chars"]
    actual = [len(line) for line in lines]
    ok = len(lines) == expected_lines and all(n == expected_chars for n in actual)
    return {
        "form": form,
        "expected_lines": expected_lines,
        "expected_chars": expected_chars,
        "actual": actual,
        "status": "pass" if ok else "fail",
    }


def check_rhyme(lines: list[str], template: dict, db: dict) -> dict:
    positions = template["rhyme_positions"]
    rhyme_chars = []
    group_sets = []
    for pos in positions:
        idx = pos - 1
        if idx >= len(lines) or not lines[idx]:
            continue
        char = lines[idx][-1]
        entries = lookup(char, db)
        groups = [e["rhyme"] for e in entries]
        rhyme_chars.append({"line": pos, "char": char, "rhyme_groups": groups})
        group_sets.append(set(groups))

    if len(group_sets) < 2:
        return {
            "expected_positions": positions,
            "first_line_rhyme": False,
            "rhyme_chars": rhyme_chars,
            "common_group": [],
            "same_group": False,
            "status": "fail",
        }

    common = set.intersection(*group_sets)
    first_groups = set()
    if lines:
        first_groups = {e["rhyme"] for e in lookup(lines[0][-1], db)}

    if not common:
        status = "unclear" if any(not gs for gs in group_sets) else "fail"
    else:
        status = "pass"

    return {
        "expected_positions": positions,
        "first_line_rhyme": bool(first_groups & common) if common else False,
        "rhyme_chars": rhyme_chars,
        "common_group": sorted(common),
        "same_group": bool(common),
        "status": status,
    }


def check_meter(lines: list[str], template: dict, db: dict) -> dict:
    chars = template["chars"]
    flexible = FLEXIBLE_5 if chars == 5 else FLEXIBLE_7
    best = None

    for pattern_name, expected_lines in template["patterns"].items():
        score = 0.0
        details = []
        uncertain = []
        fails = 0
        unclears = 0

        for i, (line, expected) in enumerate(zip(lines, expected_lines)):
            issues = []
            actual_marks = []
            line_status = "pass"
            for j, char in enumerate(line):
                exp = expected[j]
                judged = judge_tone(char, exp, j, flexible, db)
                if judged["status"] == "pass":
                    shown = judged["actual"].split("/")[0]
                    actual_marks.append(shown)
                    score += 1.0
                elif judged["status"] == "unclear":
                    actual_marks.append("?")
                    unclears += 1
                    if line_status != "fail":
                        line_status = "unclear"
                    uncertain.append(
                        {
                            "char": char,
                            "line": i + 1,
                            "position": j + 1,
                            "status": "unclear",
                            "reason": judged.get("reason", "multiple_readings"),
                            "detail": judged.get("detail", ""),
                        }
                    )
                    score += 0.5
                else:
                    actual_marks.append(judged["actual"].split("/")[0])
                    fails += 1
                    line_status = "fail"
                    issues.append(f"第{j + 1}字「{char}」期望{exp}实际{judged['actual']}")
                    score -= 1.0

            details.append(
                {
                    "line": i + 1,
                    "expected": expected,
                    "actual": "".join(actual_marks),
                    "status": line_status,
                    "issues": issues,
                }
            )

        candidate = {
            "pattern_name": pattern_name,
            "lines": details,
            "uncertain": uncertain,
            "score": score,
            "fails": fails,
            "unclears": unclears,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate

    if best is None:
        return {"pattern_name": None, "lines": [], "overall": "fail", "uncertain": []}

    if best["fails"]:
        overall = "fail"
    elif best["unclears"]:
        overall = "unclear"
    else:
        overall = "pass"

    return {
        "pattern_name": best["pattern_name"],
        "lines": best["lines"],
        "overall": overall,
        "uncertain": best["uncertain"],
    }


def validate(poem_text: str, form: str) -> dict:
    db = load_db()
    template = METER_TEMPLATES[form]
    lines = normalize(poem_text)
    structure = check_structure(lines, form, template)
    issues = []

    if structure["status"] == "fail":
        issues.append(
            {
                "priority": "fatal",
                "description": (
                    f"结构错误：期望{template['lines']}句每句{template['chars']}字，"
                    f"实际{structure['actual']}"
                ),
            }
        )
        return {
            "validation": {
                "structure": structure,
                "rhyme": {"status": "skipped"},
                "meter": {"status": "skipped"},
                "parallelism": {
                    "required": bool(template["parallelism_pairs"]),
                    "required_pairs": template["parallelism_pairs"],
                    "status": "skipped",
                },
                "issues": issues,
                "uncertain": [],
            }
        }

    rhyme = check_rhyme(lines, template, db)
    if rhyme["status"] == "fail":
        issues.append({"priority": "fatal", "description": "押韵错误：韵脚不在同一韵部"})
    elif rhyme["status"] == "unclear":
        issues.append({"priority": "major", "description": "押韵无法确定：韵脚字未收录或不唯一"})

    meter = check_meter(lines, template, db)
    for line_detail in meter.get("lines", []):
        if line_detail["status"] == "fail":
            for iss in line_detail["issues"]:
                issues.append(
                    {"priority": "major", "line": line_detail["line"], "description": iss}
                )

    parallelism = {
        "required": bool(template["parallelism_pairs"]),
        "required_pairs": template["parallelism_pairs"],
        "status": "requires_llm_review" if template["parallelism_pairs"] else "not_required",
    }

    return {
        "validation": {
            "structure": structure,
            "rhyme": rhyme,
            "meter": {
                "pattern_name": meter["pattern_name"],
                "lines": meter["lines"],
                "overall": meter["overall"],
            },
            "parallelism": parallelism,
            "issues": issues,
            "uncertain": meter.get("uncertain", []),
        }
    }


def _yaml(value, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        parts = []
        for key, item in value.items():
            compact_list = (
                isinstance(item, list)
                and item
                and all(not isinstance(x, (dict, list)) for x in item)
            )
            rendered = _yaml(item, indent + 1)
            if isinstance(item, dict) and item:
                parts.append(f"{pad}{key}:\n{rendered}")
            elif isinstance(item, list) and item and not compact_list:
                parts.append(f"{pad}{key}:\n{rendered}")
            else:
                parts.append(f"{pad}{key}: {rendered}")
        return "\n".join(parts)
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(not isinstance(x, (dict, list)) for x in value):
            return "[" + ", ".join(_scalar(x) for x in value) + "]"
        parts = []
        for item in value:
            if isinstance(item, dict):
                inner = _yaml(item, indent + 1)
                first, *rest = inner.split("\n")
                parts.append(f"{pad}- {first.lstrip()}")
                for line in rest:
                    parts.append(line)
            else:
                parts.append(f"{pad}- {_scalar(item)}")
        return "\n".join(parts)
    return _scalar(value)


def _scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or any(ch in text for ch in ":#\n[]{},"):
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Classical Chinese poetry validator")
    parser.add_argument("--poem", required=True, help="Poem text, lines separated by \\n")
    parser.add_argument("--form", required=True, choices=sorted(METER_TEMPLATES))
    parser.add_argument("--rhyme-system", default="pingshui", choices=["pingshui"])
    args = parser.parse_args()
    result = validate(args.poem, args.form)
    print(_yaml(result))


if __name__ == "__main__":
    main()
