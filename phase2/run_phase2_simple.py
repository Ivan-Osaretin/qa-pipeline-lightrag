"""
Simple Phase 2 Runner - Start Here
"""
import sys
from pathlib import Path
import json
from loguru import logger

# Add to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import HotpotQADataLoader
from phase2.graph_indexing.lightrag_graph import LightRAGGraph
from phase2.retrieval.simple_retriever import SimpleRetriever
from phase2.evaluation.basic_metrics import BasicEvaluator

def main():
    """Simple Phase 2 pipeline to get started"""
    logger.info("=" * 60)
    logger.info("PHASE 2: SIMPLE START")
    logger.info("=" * 60)
    
    # 1. Load Phase 1 data
    logger.info("\n1. Loading Phase 1 data...")
    loader = HotpotQADataLoader()
    examples = loader.load_subset("dev_subset_100")
    logger.info(f"   Loaded {len(examples)} examples")
    
    # 2. Prepare chunks (simplified)
    chunks = []
    for i, example in enumerate(examples[:20]):  # Start with 20
        # Combine context
        context_text = ""
        for _, sentences in example.context:
            context_text += ' '.join(sentences) + " "
        
        chunks.append({
            'chunk_id': f"chunk_{i}",
            'text': context_text[:1000],
            'example_id': example.id
        })
    
    logger.info(f"   Prepared {len(chunks)} chunks")
    
    # 3. Build simple graph
    logger.info("\n2. Building simple graph...")
    graph_builder = LightRAGGraph()
    graph = graph_builder.build_from_chunks(chunks)
    logger.info(f"   Graph has {graph.number_of_nodes()} nodes")
    
    # 4. Build retrieval index
    logger.info("\n3. Building retrieval index...")
    retriever = SimpleRetriever()
    retriever.build_index(chunks)
    
    # 5. Test retrieval
    logger.info("\n4. Testing retrieval...")
    test_queries = [
        "What genre of music?",
        "Which mathematician?",
        "What type of art?"
    ]
    
    for query in test_queries:
        results = retriever.retrieve(query, top_k=3)
        logger.info(f"   Query: '{query}' -> Found {len(results)} results")
        if results:
            logger.info(f"     Top: {results[0]['text'][:80]}...")
    
    # 6. Simple evaluation
    logger.info("\n5. Running simple evaluation...")
    evaluator = BasicEvaluator()
    
    # Mock predictions for now
    predictions = ["country", "Askold Khovanskii", "music"]
    gold_answers = ["country", "Askold Khovanskii", "music"]  # From examples
    
    results = evaluator.evaluate_batch(predictions, gold_answers)
    logger.info(f"   Exact Match: {results['exact_match_mean']:.3f}")
    logger.info(f"   Token Overlap: {results['overlap_mean']:.3f}")
    
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 2 SIMPLE PIPELINE COMPLETE")
    logger.info("=" * 60)
    logger.info("\nNext: Expand to full LightRAG implementation")

if __name__ == "__main__":
    main()
    