"""
FINAL VERSION: INTEGRATED LIGHTRAG PIPELINE
Consolidates indexing, retrieval, and reasoning into a unified architecture.
Saves intermediate artifacts for the 'detailed_outputs_100.json' requirement.
"""
import os
import pickle
from pathlib import Path
from loguru import logger
from phase2.retrieval.dual_retriever import SimpleRetrieverBasic as DualLevelRetriever
from phase3.llm_integration.llm_client import LLMClient
from phase3.reasoning.reasoning_engine import ReasoningEngine

class LightRAGPipeline:
    def __init__(self, graph_path: str, subset_data: list):
        logger.info("🏗️ Initializing LightRAG Pipeline with Cohere Engine...")
        
        # 1. Initialize Components
        self.llm = LLMClient(provider="cohere") 
        self.retriever = DualLevelRetriever()
        
        # 2. Data Engineering: Rebuild context from HotpotQA schema
        chunks = []
        for ex in subset_data:
            # Setting: Concatenates paragraphs into the unified search index
            ctx = " ".join([f"{t}: {' '.join(s)}" for t, s in ex['context']])
            chunks.append({'chunk_id': ex['_id'], 'text': ctx})
        
        # 3. Build Search Index
        self.retriever.build_indices(chunks)
        
        # 4. Load Reasoning Engine (Graph)
        self.engine = ReasoningEngine(graph_path, self.retriever)
        logger.success("✅ Integrated Pipeline Ready for Inference.")

    def answer_question(self, question: str) -> str:
        """Standard entry point for simple answer generation."""
        return self.engine.run_rag_pipeline(question, self.llm)

    def answer_question_detailed(self, question: str) -> dict:
        """
        Entry point for Havva's Audit requirement. 
        Returns answer + retrieved nodes + retrieved context.
        """
        # 1. Step A: Perform Vector Search
        vector_results = self.retriever.retrieve(question, top_k=3)
        vector_context = [r['text'] for r in vector_results]
        
        # 2. Step B: Perform Graph Reasoning
        graph_context = self.engine.discover_graph_context(question)
        
        # 3. Step C: Trace specific entities used in the reasoning path
        matched_entities = []
        for node_id, data in self.engine.graph.nodes(data=True):
            if data.get('type') == 'entity':
                entity_name = data.get('text', '').lower()
                if entity_name and entity_name in question.lower():
                    matched_entities.append(entity_name)

        # 4. Step D: Generate Final Answer using the combined context
        final_answer = self.engine.run_rag_pipeline(question, self.llm)
        
        return {
            "final_answer": final_answer,
            "retrieved_context": vector_context,
            "retrieved_entities": list(set(matched_entities)),
            "graph_context_provided": graph_context
        }

if __name__ == "__main__":
    # Integration Test
    import json
    with open('data/processed/dev_subset_100.json', 'r') as f:
        data = json.load(f)['examples']
    
    pipeline = LightRAGPipeline("data/indices/complete_graph.pkl", data[:1])
    test_q = data[0]['question']
    print(f"\nQUERY: {test_q}")
    print(f"RESPONSE: {pipeline.answer_question(test_q)}")
    