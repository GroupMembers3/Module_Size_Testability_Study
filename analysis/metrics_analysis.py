import os
import pandas as pd
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze

# Ensure dataset directory exists
os.makedirs("dataset", exist_ok=True)

def analyze_file(filepath):
    """Analyze a Python file for LOC, Cyclomatic Complexity, and Maintainability Index."""
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    
    raw_metrics = analyze(code)
    complexity_scores = cc_visit(code)
    cyclomatic_complexity = sum(c.complexity for c in complexity_scores) / (len(complexity_scores) or 1)
    maintainability_index = mi_visit(code, True)

    return {
        "file": os.path.basename(filepath),
        "loc": raw_metrics.loc,
        "cyclomatic_complexity": round(cyclomatic_complexity, 2),
        "maintainability_index": round(maintainability_index, 2)
    }

def analyze_project(directory="sample_project"):
    """Analyze all Python files in a given directory."""
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                results.append(analyze_file(filepath))
    return pd.DataFrame(results)

df_metrics = analyze_project()
df_metrics.to_csv("dataset/module_metrics.csv", index=False)
print("Module size & complexity metrics saved in dataset/module_metrics.csv!")
