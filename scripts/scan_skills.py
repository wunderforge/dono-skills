"""Scan all skill bundles; fail closed using agent-capability-lab's SAFE gate."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    'static_patterns_supply_chain',
    'static_patterns_prompt_injection',
    'static_patterns_data_exfiltration',
}


def is_safe(report):
    if not isinstance(report, dict):
        return False
    completeness = report.get('analysis_completeness')
    risk = report.get('risk_assessment')
    if not isinstance(completeness, dict) or not isinstance(risk, dict):
        return False
    if (report.get('execution_successful') is not True
            or completeness.get('is_complete') is not True
            or completeness.get('coverage_percent') != 100
            or risk.get('recommendation') != 'SAFE'):
        return False
    issues = report.get('issues')
    statuses = completeness.get('analyzer_statuses')
    if not isinstance(issues, list) or not isinstance(statuses, list):
        return False
    if any(not isinstance(i, dict) or str(i.get('severity', '')).upper() in {'HIGH', 'CRITICAL'} for i in issues):
        return False
    completed = {s.get('analyzer_id') for s in statuses if isinstance(s, dict) and s.get('status') == 'completed'}
    return REQUIRED <= completed


def main():
    report_dir = ROOT / 'reports'
    report_dir.mkdir(exist_ok=True)
    skills = sorted(p.parent for p in ROOT.rglob('SKILL.md')
                    if not any(part.startswith('.') for part in p.relative_to(ROOT).parts))
    if not skills:
        raise SystemExit('No skills found; refusing to pass an empty scan.')
    failed = []
    for skill in skills:
        relative = skill.relative_to(ROOT)
        report_file = report_dir / ('__'.join(relative.parts) + '.json')
        try:
            if any(p.is_symlink() for p in [skill, *skill.rglob('*')]):
                raise RuntimeError('Symlink in skill bundle')
            result = subprocess.run(
                ['skillspector', 'scan', str(skill), '--no-llm', '--format', 'json', '--output', str(report_file)],
                capture_output=True, text=True, timeout=300, check=True,
            )
            print(result.stdout)
            print(result.stderr)
            if re.search(r'ERROR|Error loading analyzer', result.stderr, re.IGNORECASE):
                raise RuntimeError('Scanner reported an analyzer error')
            report = json.loads(report_file.read_text(encoding='utf-8'))
            if not is_safe(report):
                raise RuntimeError('Complete SAFE verdict required')
            print(f'PASS {relative}')
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            failed.append(str(relative))
            print(f'FAIL {relative}: {error}')
    if failed:
        raise SystemExit(f'Failed skill scans: {", ".join(failed)}')


if __name__ == '__main__':
    main()
