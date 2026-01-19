"""
FINAL TEST - No Unicode issues
"""
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PHASE 2 - REAL DATA TEST (FINAL)")
print("=" * 70)

try:
    from phase2.graph_indexing.entity_extractor import EntityExtractor
    from phase2.graph_indexing.lightrag_graph import LightRAGGraph
    
    print("SUCCESS: All imports working")
    
    # Load data
    with open('data/processed/dev_subset_100.json', 'r') as f:
        data = json.load(f)
    
    examples = data['examples']
    print(f"Loaded {len(examples)} real HotpotQA examples")
    
    # Process first 5 now to all 100
    test_examples = examples
    
    # Create chunks
    test_chunks = []
    for i, example in enumerate(test_examples):
        context_text = ""
        for title, sentences in example.get('context', []):
            context_text += f"{title}: {' '.join(sentences)} "
        
        test_chunks.append({
            "chunk_id": f"chunk_{example['_id']}",
            "text": context_text[:500],
            "question": example['question'],
            "answer": example['answer']
        })
    
    print(f"Created {len(test_chunks)} text chunks")
    
    # Extract entities
    extractor = EntityExtractor()
    entities = extractor.extract_from_chunks(test_chunks)
    
    total_entities = sum(len(v) for v in entities.values())
    print(f"Extracted {total_entities} entities")
    
    # Build graph
    graph_builder = LightRAGGraph()
    graph = graph_builder.build_from_entities(test_chunks, entities)
    
    # Save
    graph_builder.save(Path("data/indices/real_graph.pkl"))
    print(f"Graph saved to: data/indices/real_graph.pkl")
    
    # Create ASCII-only summary
    summary = f"""
PHASE 2 - REAL DATA TEST COMPLETE
==================================
Date: 2025-12-23
Examples Processed: {len(test_examples)}
Chunks Created: {len(test_chunks)}
Entities Extracted: {total_entities}
Graph Nodes: {graph.number_of_nodes()}
Graph Edges: {graph.number_of_edges()}

SUCCESS: Real data processing working!
Ready for full-scale implementation.
"""
    
    with open("reports/phase2/real_data_test_summary.txt", "w", encoding='utf-8') as f:
        f.write(summary)
    
    print("\n" + "=" * 70)
    print("PHASE 2 REAL DATA TEST - COMPLETE SUCCESS!")
    print("=" * 70)
    print(f"Processed {len(test_examples)} real HotpotQA examples")
    print(f"Extracted {total_entities} real entities")
    print(f"Built graph with {graph.number_of_nodes()} nodes")
    print(f"Graph saved for future use")
    print("\nREADY TO EMAIL HAVVA WITH REAL PROGRESS!")
    print("=" * 70)
    
    # Show what we can do now
    print("\n" + "=" * 70)
    print("IMMEDIATE NEXT STEPS POSSIBLE:")
    print("=" * 70)
    print("1. Process ALL 100 examples (not just 5)")
    print("2. Implement BM25 retrieval on the chunks")
    print("3. Add vector embeddings for semantic search")
    print("4. Create evaluation on actual questions")
    print("=" * 70)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()