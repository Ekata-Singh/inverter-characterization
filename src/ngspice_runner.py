"""Fill netlist templates, run ngspice in batch mode, and read .meas results."""
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

NGSPICE = shutil.which("ngspice")
TOKEN_RE = re.compile(r"@[A-Z_]+@")
# Matches lines such as "tphl                =  1.63e-11 targ= ..."
MEAS_RE = re.compile(r"^(\w+)\s*=\s*([-+]?\d+\.?\d*(?:[eE][-+]?\d+)?)", re.MULTILINE)


def fill_template(template_path, tokens):
    """Replace @KEY@ tokens in a netlist template. Fails if any token is left over."""
    text = Path(template_path).read_text()
    for key, value in tokens.items():
        text = text.replace(f"@{key}@", str(value))
    leftover = TOKEN_RE.findall(text)
    if leftover:
        raise ValueError(f"Unfilled tokens in {template_path}: {sorted(set(leftover))}")
    return text


def parse_measurements(log_text):
    """Return {measure_name: value} for every .meas line in an ngspice log."""
    return {m.group(1).lower(): float(m.group(2)) for m in MEAS_RE.finditer(log_text)}


def run_netlist(netlist_text):
    """Run one netlist through ngspice and return its .meas results."""
    if NGSPICE is None:
        raise RuntimeError("ngspice not found. Install it, e.g. `sudo apt install ngspice`.")
    with tempfile.TemporaryDirectory() as tmp:
        cir = Path(tmp) / "sim.cir"
        log = Path(tmp) / "sim.log"
        cir.write_text(netlist_text)
        subprocess.run([NGSPICE, "-b", "-o", str(log), str(cir)],
                       check=True, capture_output=True, text=True)
        return parse_measurements(log.read_text())
