#!/usr/bin/env python
"""
Setup script for Phase 1 - Downloads and processes HotpotQA data
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from data_loader import HotpotQADataLoader
    print("✅ Data loader imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure src/data_loader.py exists")
    sys.exit(1)

def main():
    print("=" * 60)
    print("PHASE 1: SETUP DATA PIPELINE")
    print("=" * 60)
    
    # Initialize loader
    loader = HotpotQADataLoader()
    
    try:
        # Load existing data
        print("\n📊 Loading existing data...")
        subset = loader.load_subset("dev_subset_100")
        print(f"✅ Successfully loaded {len(subset)} examples")
        
        # Show first example
        if subset:
            first_ex = subset[0]
            print(f"\n📄 First example:")
            print(f"   Question: {first_ex.get('question', 'N/A')[:80]}...")
            print(f"   Answer: {first_ex.get('answer', 'N/A')}")
            print(f"   Type: {first_ex.get('type', 'N/A')}")
            print(f"   Context paragraphs: {len(first_ex.get('context', []))}")
        
        print("\n" + "=" * 60)
        print("✅ DATA PIPELINE SETUP COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
