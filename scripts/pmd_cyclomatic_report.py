import subprocess
import os
import csv
import re

# === CONFIGURATION ===
RULESET_PATH = r"C:\Users\xayit\Uni\Bachelor\scripts\cyclomatic_ruleset.xml"
SOURCE_DIR = r"C:\Users\xayit\Uni\Bachelor\all_patched_classes"
OUTPUT_FILE = "cyclomatic_report.csv"

# === RUN PMD ===
print("Running PMD...")
result = subprocess.run(
    ["pmd", "check", "-d", SOURCE_DIR, "-R", RULESET_PATH, "-f", "text"],
    capture_output=True,
    text=True,
)

# Handle return codes: 0 (OK), 4 (violations found)
if result.returncode not in (0, 4):
    print("PMD failed with errors:\n", result.stderr)
    exit(1)

output = result.stdout

# === PARSE OUTPUT ===
pattern = re.compile(
    r"^(.*\.java):\d+:.*The class '(.*?)' has a total cyclomatic complexity of (\d+)"
)

entries = []

for line in output.splitlines():
    match = pattern.match(line)
    if match:
        file_path, class_name, complexity = match.groups()
        rel_path = os.path.relpath(file_path, SOURCE_DIR)
        entries.append((rel_path, class_name, int(complexity)))

# === WRITE CSV ===
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["File", "Class", "Cyclomatic Complexity"])
    writer.writerows(entries)

# Use a simple message for the output to avoid Unicode errors
print(f"\nReport saved to: {OUTPUT_FILE} with {len(entries)} classes analyzed.")
