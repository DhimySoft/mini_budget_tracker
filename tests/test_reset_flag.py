import subprocess
import os
import sqlite3

def test_reset_flag_creates_db_and_data(tmp_path):
    # Run reset flag in a clean temporary directory
    db_file = tmp_path / "budget.db"
    env = os.environ.copy()
    env["DB_FILE"] = str(db_file)  # optional if you later support custom DB location

    result = subprocess.run(
        ["python", "-m", "mini_budget_tracker.budget_tracker", "--reset"],
        capture_output=True,
        text=True,
        env=env
    )

    # Check process finished successfully
    assert result.returncode == 0
    assert "Database reset" in result.stdout

    # Verify database exists and has data
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 30
