#!/usr/bin/env python
"""
Simple data analysis for Phase 1
"""
import json
from pathlib import Path

def analyze_dataset():
    print("=" * 60)
    print("PHASE 1 DATA ANALYSIS")
    print("=" * 60)
    
    data_path = Path("data/processed/dev_subset_100.json")
    
    if not data_path.exists():
        print("❌ Dataset not found.")
        return
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Get examples
    examples = data.get('examples', [])
    
    print(f"📊 Loaded {len(examples)} examples")
    
    # Simple statistics
    print(f"\n📈 Dataset Statistics:")
    print(f"   • Total examples: {len(examples)}")
    
    # Count types
    types = {}
    for item in examples:
        t = item.get('type', 'unknown')
        types[t] = types.get(t, 0) + 1
    
    for t, count in types.items():
        print(f"   • {t}: {count}")
    
    print(f"\n✅ Analysis complete - Phase 1 ready!")

if __name__ == "__main__":
    analyze_dataset()
