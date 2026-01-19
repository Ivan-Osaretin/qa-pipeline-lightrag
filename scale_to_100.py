# Create scale_to_100.py
"""
Scale Phase 2 to ALL 100 examples
"""
import json
from pathlib import Path
from phase2.graph_indexing.entity_extractor import EntityExtractor
from phase2.graph_indexing.lightrag_graph import LightRAGGraph

# Load ALL 100 examples
with open('data/processed/dev_subset_100.json', 'r') as f:
    data = json.load(f)

all_examples = data['examples']
print(f"Processing ALL {len(all_examples)} examples...")

# Process in batches of 20
for batch_start in range(0, len(all_examples), 20):
    batch = all_examples[batch_start:batch_start + 20]
    # Your processing code here
    print(f"Processed batch {batch_start//20 + 1}/5")