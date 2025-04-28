import subprocess
import os
import csv


def get_bug_ids(project_dir):
    """
    Reads bug IDs from the active-bugs.csv file in the project's directory.

    Parameters:
        project_dir (str): The directory of the project containing active-bugs.csv.

    Returns:
        list of int: List of bug IDs.
    """
    bug_ids = []
    csv_path = os.path.join(project_dir, "active-bugs.csv")

    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bug_ids.append(int(row["bug.id"]))

    return bug_ids


def checkout_defects4j(project, bug_id, base_dir):
    """
    Checkout both buggy and fixed versions of a specified Defects4J project bug.

    Parameters:
        project (str): The name of the Defects4J project (e.g., "Lang", "Math").
        bug_id (int): The bug ID number.
        base_dir (str): The base directory where the project versions will be saved.
    """
    for version in ["b", "f"]:  # "b" for buggy, "f" for fixed
        # Construct the version ID and work directory
        version_id = f"{bug_id}{version}"
        work_dir = os.path.join(base_dir, project, f"{project}_{version_id}")

        # Make sure the directory exists
        os.makedirs(work_dir, exist_ok=True)

        # Defects4J checkout command
        command = [
            "defects4j",
            "checkout",
            "-p",
            project,
            "-v",
            version_id,
            "-w",
            work_dir,
        ]

        try:
            print(f"Checking out {project} version {version_id} into {work_dir}...")
            # Run the command
            subprocess.run(command, check=True)
            print(f"Successfully checked out {project} version {version_id}")
        except subprocess.CalledProcessError as e:
            print(f"Error checking out {project} version {version_id}: {e}")


# Configuration
projects = ["Codec"]

projects_dir = "/mnt/c/Users/xayit/defects4j/framework/projects"
base_dir = "/mnt/c/Users/xayit/Uni/Bachelor/temp"

# Run the checkout for each project and bug ID
for project in projects:
    project_dir = os.path.join(projects_dir, project)
    bug_ids = get_bug_ids(project_dir)
    for bug_id in bug_ids:
        checkout_defects4j(project, bug_id, base_dir)
