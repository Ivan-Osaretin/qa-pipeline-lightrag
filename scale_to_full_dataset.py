"""
SCALE TO FULL DATASET - Definitive Implementation
Processes all 100 HotpotQA examples with proper dict handling.
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from phase2.graph_indexing.entity_extractor import EntityExtractor
from phase2.graph_indexing.lightrag_graph import LightRAGGraph

def run_scaling():
    print(f"🚀 Scaling started at {datetime.now()}")
    
    # 1. Loads correctly using 'examples' key
    with open('data/processed/dev_subset_100.json', 'r') as f:
        raw_data = json.load(f)
    examples = raw_data['examples']
    
    # 2. Extracts Chunks
    chunks = []
    for ex in examples:
        ctx = " ".join([f"{t}: {' '.join(s)}" for t, s in ex['context']])
        chunks.append({"chunk_id": ex['_id'], "text": ctx[:1200], "answer": ex['answer']})
    
    # 3. Process Entities
    extractor = EntityExtractor()
    entities = extractor.extract_from_chunks(chunks)
    
    # 4. Builds and Saves Graph
    # Fixed: Passing graph_name correctly
    graph_builder = LightRAGGraph(graph_name="hotpotqa_full_100")
    graph_builder.build_from_entities(chunks, entities)
    graph_builder.save(Path("data/indices/complete_graph.pkl"))
    
    print(f"✅ Scaling Complete. Processed {len(examples)} items.")

if __name__ == "__main__":
    run_scaling()