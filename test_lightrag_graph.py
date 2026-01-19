"""
STANDALONE TEST for LightRAG Graph
Run this from root directory
"""
import sys
from pathlib import Path

# Add phase2 to path so imports work
sys.path.append(str(Path(__file__).parent / "phase2" / "graph_indexing"))

print("=" * 60)
print("🧪 STANDALONE LIGHTRAG GRAPH TEST")
print("=" * 60)

# Now import
try:
    from entity_extractor import EntityExtractor
    from lightrag_graph import LightRAGGraph
    
    print("✅ Imports successful!")
    
    # Test with sample data
    print("\n📊 Testing with sample data...")
    
    # Create test chunks
    test_chunks = [
        {
            "chunk_id": "test_1",
            "text": "Askold Khovanskii is a mathematician who worked on algebraic geometry at Moscow State University.",
            "question": "Which mathematician worked with algebraic geometry?",
            "answer": "Askold Khovanskii"
        },
        {
            "chunk_id": "test_2", 
            "text": "The Consul and Arlecchino are both musical works composed in the 20th century.",
            "question": "What type of art is common between The Consul and Arlecchino?",
            "answer": "music"
        }
    ]
    
    # Extract entities
    extractor = EntityExtractor()
    entities = extractor.extract_from_chunks(test_chunks)
    
    print(f"📈 Extracted {sum(len(v) for v in entities.values())} entities")
    
    # Build graph
    graph_builder = LightRAGGraph()
    graph = graph_builder.build_from_entities(test_chunks, entities)
    
    # Test queries
    print("\n🔍 Testing graph queries:")
    test_queries = ["Khovanskii", "mathematician", "Moscow", "music", "century"]
    
    for query in test_queries:
        results = graph_builder.query(query)
        print(f"  '{query}': Found {len(results)} results")
        if results:
            print(f"    Top: {results[0]['text'][:50]}...")
    
    # Save graph
    graph_builder.save(Path("data/indices/test_graph.pkl"))
    print(f"\n💾 Graph saved to: data/indices/test_graph.pkl")
    
    print("\n✅ Graph test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n💡 Try running from root directory with:")
    print("   python test_lightrag_graph.py")
except Exception as e:
    print(f"❌ Error during test: {e}")
    import traceback
    traceback.print_exc()