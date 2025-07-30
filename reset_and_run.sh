#!/bin/bash
python3 reset_db.py
python3 budget_tracker.py
#This deletes the old database, creates a fresh one, and launches your budget tracker.
# The main.py should check if the database is empty before adding sample data to avoid duplicates.