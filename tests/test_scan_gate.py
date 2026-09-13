import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('gate', Path(__file__).resolve().parents[1] / 'scripts/scan_skills.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class ScanGateTests(unittest.TestCase):
    def setUp(self):
        self.report = {
            'execution_successful': True,
            'risk_assessment': {'recommendation': 'SAFE'},
            'issues': [],
            'analysis_completeness': {
                'is_complete': True, 'coverage_percent': 100,
                'analyzer_statuses': [{'analyzer_id': name, 'status': 'completed'} for name in gate.REQUIRED],
            },
        }

    def test_complete_safe(self):
        self.assertTrue(gate.is_safe(self.report))

    def test_rejects_incomplete_or_unsafe(self):
        for section, key, value in [
            (None, 'execution_successful', False),
            ('risk_assessment', 'recommendation', 'CAUTION'),
            ('analysis_completeness', 'is_complete', False),
            ('analysis_completeness', 'coverage_percent', 85.7),
            ('analysis_completeness', 'analyzer_statuses', []),
            (None, 'issues', [{'severity': 'HIGH'}]),
            (None, 'issues', [{'severity': 'CRITICAL'}]),
        ]:
            with self.subTest(key=key, value=value):
                report = copy.deepcopy(self.report)
                (report if section is None else report[section])[key] = value
                self.assertFalse(gate.is_safe(report))

    def test_rejects_missing_and_malformed_reports(self):
        for report in [None, {}, [], {'risk_assessment': None}]:
            self.assertFalse(gate.is_safe(report))


if __name__ == '__main__':
    unittest.main()
