"""Measure static leakage power for both input states.

Example:
    python src/run_leakage.py
"""
from measure import measure_leakage


def main():
    low = measure_leakage(input_high=False)
    high = measure_leakage(input_high=True)
    print(f"leakage power: input low = {low:.4f} nW, input high = {high:.4f} nW")


if __name__ == "__main__":
    main()
