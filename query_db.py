import sqlite3
import json

db_path = 'backend/agentprobe.db'
session_id = 'b77c8238-b736-4827-ac84-5fae3b413dc6'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"--- Session: {session_id} ---")
cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
session = cursor.fetchone()
if session:
    print(f"ID: {session[0]}")
    print(f"Archetype: {session[1]}")
    print(f"Selected Traps: {session[2]}")
    print(f"Created At: {session[3]}")
else:
    print("Session not found.")

print(f"\n--- Trap Logs for {session_id} ---")
cursor.execute("SELECT * FROM trap_logs WHERE session_id = ?", (session_id,))
logs = cursor.fetchall()
if logs:
    for log in logs:
        print(log)
else:
    print("No trap logs found.")

conn.close()
