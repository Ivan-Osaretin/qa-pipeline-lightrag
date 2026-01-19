"""
PROPER TEST RUNNER for LightRAG Graph
"""
import sys
from pathlib import Path
import json

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("🧪 PROPER LIGHTRAG GRAPH TEST")
print("=" * 70)

try:
    # Import using absolute import
    from phase2.graph_indexing.entity_extractor import EntityExtractor
    from phase2.graph_indexing.lightrag_graph import LightRAGGraph
    
    print("✅ Imports successful!")
    
    # Test with ACTUAL HotpotQA data
    print("\n📊 Loading ACTUAL HotpotQA data...")
    
    with open('data/processed/dev_subset_100.json', 'r') as f:
        data = json.load(f)
    
    examples = data['examples']
    print(f"✅ Loaded {len(examples)} real examples")
    
    # Take first 5 examples for testing
    test_examples = examples[:5]
    
    # Create chunks from examples
    test_chunks = []
    for i, example in enumerate(test_examples):
        # Combine context text
        context_text = ""
        for title, sentences in example.get('context', []):
            context_text += f"{title}: {' '.join(sentences)} "
        
        test_chunks.append({
            "chunk_id": f"chunk_{example['_id']}",
            "text": context_text[:500],  # First 500 chars
            "question": example['question'],
            "answer": example['answer'],
            "type": example.get('type', 'unknown'),
            "metadata": {
                "example_id": example['_id'],
                "level": example.get('level', 'unknown')
            }
        })
    
    print(f"📄 Created {len(test_chunks)} chunks from real data")
    
    # Extract entities
    print("\n🔍 Extracting entities from real data...")
    extractor = EntityExtractor()
    entities = extractor.extract_from_chunks(test_chunks)
    
    total_entities = sum(len(v) for v in entities.values())
    print(f"📈 Extracted {total_entities} entities from real data")
    
    # Show some entities
    print("\n📋 Sample entities found:")
    for chunk_id, entity_list in list(entities.items())[:2]:  # First 2 chunks
        print(f"  Chunk: {chunk_id}")
        for entity in entity_list[:3]:  # First 3 entities
            print(f"    • {entity.text} ({entity.label})")
    
    # Build graph
    print("\n🕸️ Building knowledge graph...")
    graph_builder = LightRAGGraph()
    graph = graph_builder.build_from_entities(test_chunks, entities)
    
    # Test queries with ACTUAL questions
    print("\n🔍 Testing graph queries with real questions:")
    
    # Get questions from the examples
    test_queries = [
        test_examples[0]['question'][:30] + "...",  # First question
        "country",  # Common in answers
        "music",    # Common topic
        "artist"    # Common entity
    ]
    
    for query in test_queries:
        results = graph_builder.query(query)
        print(f"  Query: '{query}'")
        print(f"    Found: {len(results)} results")
        if results:
            for i, result in enumerate(results[:2]):  # Show top 2
                print(f"    {i+1}. {result['text'][:60]}...")
    
    # Save graph
    graph_builder.save(Path("data/indices/real_graph.pkl"))
    print(f"\n💾 Graph saved to: data/indices/real_graph.pkl")
    
    # Create a summary file
    summary = f"""
PHASE 2 - REAL DATA TEST COMPLETE
==================================
Date: 2025-12-23
Examples Processed: {len(test_examples)}
Chunks Created: {len(test_chunks)}
Entities Extracted: {total_entities}
Graph Nodes: {graph.number_of_nodes()}
Graph Edges: {graph.number_of_edges()}

✅ REAL DATA PROCESSING SUCCESSFUL!
Ready for full-scale implementation.
"""
    
    with open("reports/phase2/real_data_test_summary.txt", "w") as f:
        f.write(summary)
    
    print("\n" + "=" * 70)
    print("🎉 REAL DATA TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"✅ Processed {len(test_examples)} real HotpotQA examples")
    print(f"✅ Extracted {total_entities} real entities")
    print(f"✅ Built graph with {graph.number_of_nodes()} nodes")
    print(f"✅ Tested queries with real questions")
    print(f"✅ Saved results and summary")
    print("\n📧 READY TO EMAIL HAVVA WITH REAL PROGRESS!")
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Checking module structure...")
    
    # Check if files exist
    files_to_check = [
        "phase2/graph_indexing/entity_extractor.py",
        "phase2/graph_indexing/lightrag_graph.py"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing!")
    
    print("\nTry creating the files first:")
    print("1. Create phase2/graph_indexing/entity_extractor.py")
    print("2. Create phase2/graph_indexing/lightrag_graph.py")
    
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()