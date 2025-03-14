import os
import subprocess
import pandas as pd

# Ensure dataset directory exists
os.makedirs("dataset", exist_ok=True)

def compute_coverage(directory="sample_project"):
    """Run pytest-cov using Python module execution."""
    try:
        result = subprocess.run(["python", "-m", "pytest", "--cov=" + directory], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "TOTAL" in line:
                return float(line.split()[-1].replace("%", ""))
    except Exception as e:
        print("Error running pytest-cov:", str(e))
    return None

def compute_mutation_score(directory="sample_project"):
    """Run MutPy using Python module execution."""
    try:
        result = subprocess.run(["python", "-m", "mutpy", "--target", directory, "--unit-test"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "Mutation score" in line:
                return float(line.split()[-1].replace("%", ""))
    except Exception as e:
        print("Error running MutPy:", str(e))
    return None

# Run testability metrics
coverage = compute_coverage()
mutation_score = compute_mutation_score()

# Store results
df_testability = pd.DataFrame([{"code_coverage": coverage, "mutation_score": mutation_score}])
df_testability.to_csv("dataset/testability_metrics.csv", index=False)

print("Testability metrics saved in dataset/testability_metrics.csv!")
