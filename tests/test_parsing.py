"""Tests for template filling and .meas parsing. These do not need ngspice.

Run with: python -m unittest discover tests
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ngspice_runner import fill_template, parse_measurements  # noqa: E402

SAMPLE_LOG = """\
Circuit: sim.cir
tphl                =  1.631703e-11 targ=  1.041317e-09 trig=  1.025000e-09
tplh                =  1.631703e-11 targ=  1.009132e-08 trig=  1.007500e-08
ileak               = -3.300000e-12
"""


class ParseMeasurementsTest(unittest.TestCase):
    def test_reads_all_measure_values(self):
        results = parse_measurements(SAMPLE_LOG)
        self.assertAlmostEqual(results["tphl"], 1.631703e-11)
        self.assertAlmostEqual(results["tplh"], 1.631703e-11)
        self.assertAlmostEqual(results["ileak"], -3.3e-12)

    def test_ignores_non_measure_lines(self):
        self.assertEqual(set(parse_measurements("Circuit: sim.cir\n")), set())


class FillTemplateTest(unittest.TestCase):
    def test_replaces_all_tokens(self):
        with tempfile.NamedTemporaryFile("w", suffix=".tpl", delete=False) as f:
            f.write("VIN in 0 PULSE(0 @VDD@ 1n @SLEW@ @SLEW@ 9n 20n)\n")
        text = fill_template(f.name, {"VDD": 1.8, "SLEW": "50p"})
        self.assertIn("PULSE(0 1.8 1n 50p 50p 9n 20n)", text)

    def test_fails_on_leftover_token(self):
        with tempfile.NamedTemporaryFile("w", suffix=".tpl", delete=False) as f:
            f.write("CL out 0 @CLOAD@\n")
        with self.assertRaises(ValueError):
            fill_template(f.name, {"VDD": 1.8})


if __name__ == "__main__":
    unittest.main()
