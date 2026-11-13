"""Measurement functions built on the netlist templates."""
from pathlib import Path

from ngspice_runner import fill_template, run_netlist

NETLIST_DIR = Path(__file__).resolve().parent.parent / "netlists"
VDD = 1.8  # volts


def measure_delay(cload_ff, slew_ps, vdd=VDD):
    """Return (tphl_ps, tplh_ps) for one load (fF) and input slew (ps)."""
    netlist = fill_template(
        NETLIST_DIR / "delay.cir.tpl",
        {
            "VDD": vdd,
            "HALF": vdd / 2,
            "SLEW": f"{slew_ps}p",
            "CLOAD": f"{cload_ff}f",
        },
    )
    results = run_netlist(netlist)
    missing = {"tphl", "tplh"} - results.keys()
    if missing:
        raise RuntimeError(f"Measurements {sorted(missing)} missing at {cload_ff} fF, {slew_ps} ps")
    return results["tphl"] * 1e12, results["tplh"] * 1e12


def measure_leakage(input_high, vdd=VDD):
    """Return static leakage power in nW with the input held high or low."""
    netlist = fill_template(
        NETLIST_DIR / "leakage.cir.tpl",
        {"VDD": vdd, "VIN": vdd if input_high else 0},
    )
    results = run_netlist(netlist)
    if "ileak" not in results:
        raise RuntimeError("Leakage measurement 'ileak' missing from ngspice output")
    # The supply sources current, so the reported value is negative; power is |I| * VDD.
    return abs(results["ileak"]) * vdd * 1e9
