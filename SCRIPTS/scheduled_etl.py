from pathlib import Path
import subprocess
import sys

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "SCRIPTS"

print("=" * 60)
print("AUTOMATED MUTUAL FUND ETL")
print("=" * 60)

def run_script(script_name):
    script_path = SCRIPTS_DIR / script_name

    print(f"\nRunning: {script_name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True
    )

    print(f"Completed: {script_name}")
    return result


# Run existing ETL pipeline
run_script("run_pipeline.py")

print("\n" + "=" * 60)
print("SCHEDULED ETL COMPLETED SUCCESSFULLY")
print("=" * 60)