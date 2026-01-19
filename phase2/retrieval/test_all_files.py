"""
Test that all Phase 2 files exist
"""
import sys
from pathlib import Path

print("=" * 60)
print("TESTING PHASE 2 FILES EXIST")
print("=" * 60)

# List of required files
required_files = [
    "phase2/graph_indexing/lightrag_graph.py",
    "phase2/retrieval/simple_retriever.py", 
    "phase2/evaluation/basic_metrics.py",
    "src/data_loader.py",
    "data/processed/dev_subset_100.json"
]

all_exist = True
for file_path in required_files:
    if Path(file_path).exists():
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - MISSING!")
        all_exist = False

print("\n" + "=" * 60)
if all_exist:
    print("✅ ALL FILES EXIST! Ready to run Phase 2.")
else:
    print("❌ SOME FILES MISSING. Create them first.")
print("=" * 60)