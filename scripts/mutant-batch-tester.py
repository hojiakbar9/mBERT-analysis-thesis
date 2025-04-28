import os
import shutil
import subprocess
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import time

# ===== CONFIG =====
CSV_FILE = '/defects4j/projects/codec/codec_13/generated-mutants-full/double-metaphone/-compilation.csv'
MUTANTS_DIR = '/defects4j/projects/codec/codec_13/generated-mutants-full/double-metaphone/'
PROJECT_DIR = '/defects4j/projects/codec/codec_13'
PROJECT_NAME = 'codec_13'
MUTATED_CLASS_NAME = 'DoubleMetaphone.java'
RELATIVE_PATH = 'src/main/java/org/apache/commons/codec/language/DoubleMetaphone.java'
LOG_FILE = '/defects4j/projects/codec/codec_13/generated-mutants-full/mutants_batch_log.txt'

BATCH_SIZE = 150
MAX_WORKERS = 8
TIMEOUT = 200

# ===== READ MUTANTS =====
def read_compilable_mutants(csv_file):
    mutants = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['compile'].strip() == '1':
                mutants.append(row['id'].strip())
    return mutants

# ===== BATCH PROCESSING =====
def create_batches(mutants, batch_size):
    return [mutants[i:i + batch_size] for i in range(0, len(mutants), batch_size)]

def run_batch(batch_mutants):
    batch_id = f"batch_{batch_mutants[0]}_{batch_mutants[-1]}"
    temp_dir = Path(f"/defects4j/projects/tmp_batches/{batch_id}")
    worker_project_dir = temp_dir / PROJECT_NAME
    
    try:
        shutil.copytree(PROJECT_DIR, worker_project_dir)
        print(f"[{batch_id}] Project copied to {worker_project_dir}")

        results = []
        for mutant_id in batch_mutants:
            result = run_mutant_test(worker_project_dir, mutant_id, batch_id)
            results.append(result)
        
        return f"[{batch_id}] Completed:\n" + "\n".join(results)

    except Exception as e:
        return f"[{batch_id}] EXCEPTION: {str(e)}"
    
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[{batch_id}] Cleaned up temp dir")

def run_mutant_test(worker_project_dir, mutant_id, batch_id):
    mutant_file = Path(MUTANTS_DIR) / mutant_id / MUTATED_CLASS_NAME
    target_file = worker_project_dir / RELATIVE_PATH

    if not target_file.exists():
        return f"[{batch_id} - Mutant {mutant_id}] ERROR: Target file not found"

    try:
        shutil.copy(mutant_file, target_file)
    except Exception as e:
        return f"[{batch_id} - Mutant {mutant_id}] Failed to replace file: {str(e)}"

    # Run defects4j test with timeout
    command = f"defects4j test -w {worker_project_dir}"
    try:
        completed = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=TIMEOUT)
        output = completed.stdout
        exit_code = completed.returncode

        return f"[{batch_id} - Mutant {mutant_id}] Exit Code: {exit_code}\n{output}"

    except subprocess.TimeoutExpired:
        return f"[{batch_id} - Mutant {mutant_id}] TIMEOUT after {TIMEOUT} seconds"
    except Exception as e:
        return f"[{batch_id} - Mutant {mutant_id}] ERROR: {str(e)}"

# ===== LOGGING =====
def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(line + '\n')

# ===== MAIN =====
def main():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    mutants = read_compilable_mutants(CSV_FILE)
    log(f"Found {len(mutants)} compilable mutants")

    batches = create_batches(mutants, BATCH_SIZE)
    log(f"Created {len(batches)} batches (batch size: {BATCH_SIZE})")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(run_batch, batch): batch for batch in batches}
        
        for future in as_completed(futures):
            result = future.result()
            log(result)

    log("All batches completed.")

if __name__ == "__main__":
    main()
