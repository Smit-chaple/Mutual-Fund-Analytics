import subprocess
import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "SCRIPTS"


# ============================================================
# RUN SCRIPT
# ============================================================

def run_script(script_name):

    script_path = SCRIPTS_DIR / script_name

    print("\n" + "=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found: {script_path}"
        )

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed."
        )

    print(
        f"[SUCCESS] {script_name} completed successfully."
    )


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("MUTUAL FUND ANALYTICS - AUTOMATED PIPELINE")
    print("=" * 60)

    try:

        # ----------------------------------------------------
        # 1. EXTRACT
        # ----------------------------------------------------

        run_script("data_ingestion.py")


        # ----------------------------------------------------
        # 2. TRANSFORM / CLEAN
        # ----------------------------------------------------

        run_script("data_cleaning.py")


        # ----------------------------------------------------
        # 3. LOAD DATABASE
        # ----------------------------------------------------

        run_script("load_database.py")


        # ----------------------------------------------------
        # 4. FETCH LIVE NAV
        # ----------------------------------------------------

        run_script("live_nav_fetch.py")


        # ----------------------------------------------------
        # 5. GENERATE REPORT + SEND EMAIL
        # ----------------------------------------------------

        run_script("weekly_email_report.py")


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print("\nLive NAV updated.")
        print("SQLite database updated.")
        print("Weekly report generated.")
        print("Email sent successfully.")


    except Exception as e:

        print("\n" + "=" * 60)
        print("PIPELINE FAILED")
        print("=" * 60)

        print(f"\nError: {e}")

        sys.exit(1)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    main()