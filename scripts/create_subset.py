import json
import random
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("PHASE 1: Create Subset")
print("=" * 60)

# Paths
raw_file = Path("data/raw/hotpot_dev_distractor_v1.json")
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True)

if not raw_file.exists():
    print("✗ Raw data not found. Run download first.")
    exit(1)

print("Loading data...")
with open(raw_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data)} examples")

# Create balanced subset of 100 examples
random.seed(42)  # For reproducibility

# Count types
comparison = [ex for ex in data if ex.get('type') == 'comparison']
bridge = [ex for ex in data if ex.get('type') == 'bridge']

print(f"Comparison questions: {len(comparison)}")
print(f"Bridge questions: {len(bridge)}")

# Take 50 of each for 100 total
subset = []
subset.extend(random.sample(comparison, min(50, len(comparison))))
subset.extend(random.sample(bridge, min(50, len(bridge))))
random.shuffle(subset)

print(f"Created subset: {len(subset)} examples")

# Save subset
output_file = processed_dir / "dev_subset_100.json"
metadata = {
    'metadata': {
        'name': 'dev_subset_100',
        'total_examples': len(subset),
        'creation_date': datetime.now().isoformat(),
        'description': 'Balanced subset of HotpotQA (50 comparison, 50 bridge)',
        'source': 'HotpotQA development set'
    },
    'examples': subset
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print(f"✓ Saved subset to: {output_file}")
print(f"✓ File size: {output_file.stat().st_size / 1024:.1f} KB")

# Also save a CSV-like version for viewing
sample_file = processed_dir / "sample_questions.txt"
with open(sample_file, 'w', encoding='utf-8') as f:
    f.write("SAMPLE QUESTIONS FROM SUBSET\n")
    f.write("=" * 50 + "\n\n")
    for i, ex in enumerate(subset[:10], 1):
        f.write(f"Example {i}:\n")
        f.write(f"  ID: {ex.get('_id', 'N/A')}\n")
        f.write(f"  Type: {ex.get('type', 'N/A')}\n")
        f.write(f"  Question: {ex.get('question', 'N/A')}\n")
        f.write(f"  Answer: {ex.get('answer', 'N/A')}\n")
        f.write(f"  Level: {ex.get('level', 'N/A')}\n")
        f.write("-" * 50 + "\n\n")

print(f"✓ Created sample file: {sample_file}")

print("=" * 60)
print("PHASE 1 COMPLETE!")
print(f"  • Downloaded: {len(data)} examples")
print(f"  • Created subset: {len(subset)} examples")
print(f"  • Balanced: 50 comparison, 50 bridge")
print(f"  • Saved to: data/processed/")
print("=" * 60)
