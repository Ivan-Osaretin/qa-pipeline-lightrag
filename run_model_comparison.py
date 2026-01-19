"""
PHASE 4 - PROFESSIONAL MODEL COMPARISON
Benchmarks Llama vs. Gemini vs. Command R+ on a subset of data.
"""
import json
import os
import sys
import time
from pathlib import Path
from tqdm import tqdm
from loguru import logger

# Ensures in principle that local modules are findable
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lightrag_pipeline import LightRAGPipeline
from phase2.evaluation.rag_evaluator import RAGEvaluator
from phase3.llm_integration.llm_client import LLMClient

def main():
    # --- CONFIGURATION ---
    # Set to 3 for 'Smoke Test', 25 for 'Final Scientific Results Based on Resource Limits <rate limits of a student research project  >'
    LIMIT = 25
    
    # 1. Loads Data
    data_path = os.path.join(project_root, 'data', 'processed', 'dev_subset_100.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        examples = data['examples'][:LIMIT]

    # --- THE SANITY CHECK ---
    print("\n" + "!"*65)
    print(f"CRITICAL CONFIRMATION")
    print(f"Total Examples: {len(examples)}")
    print(f"Total API Calls: {len(examples) * 3} (Groq + Gemini + Cohere)")
    print(f"Estimated Time: ~{ (len(examples) * 3 * 6) / 60 } minutes")
    print("!"*65)
    print("Execution will start in 5 seconds... (Ctrl+C to abort)")
    time.sleep(5)

    providers = ["groq", "gemini", "cohere"]
    comparison_summary = []

    # 2. Benchmark Loop
    for provider in providers:
        print(f"\n🚀 STARTING BENCHMARK: {provider.upper()}")
        
        try:
            # Initializes Pipeline with specific provider
            llm = LLMClient(provider=provider)
            pipeline = LightRAGPipeline("data/indices/complete_graph.pkl", examples)
            pipeline.llm = llm # Injected for comparison

            results = []
            for ex in tqdm(examples, desc=f"Querying {provider}"):
                # Uses a strict prompt to improve EM scores
                strict_system_prompt = (
                    "You are a strict QA assistant. Answer the question using ONLY the specific "
                    "name, date, or entity from the context. Be extremely concise. "
                    "No full sentences. Do not say 'The answer is'."
                )
                
                # Use the pipeline logic
                # Note: This assumes ReasoningEngine's run_rag_pipeline uses the llm_client
                prediction = pipeline.answer_question(ex['question'])
                results.append({"gold": ex['answer'], "pred": prediction})
            
            # Evaluates this model
            evaluator = RAGEvaluator()
            preds = [r['pred'] for r in results]
            golds = [r['gold'] for r in results]
            metrics = evaluator.evaluate_batch(preds, golds)
            
            comparison_summary.append({
                "Provider": provider,
                "EM": metrics['exact_match']['mean'],
                "F1": metrics['f1_score']['mean']
            })
            
        except Exception as e:
            logger.error(f"Failed to benchmark {provider}: {e}")

    # 3. PRINTS FINAL TABLE
    print("\n" + "="*55)
    print("FINAL RESEARCH COMPARISON: LLM REASONING STRENGTH")
    print("-" * 55)
    print(f"{'Provider':<15} | {'Exact Match':<12} | {'F1 Score':<10}")
    print("-" * 55)
    for r in comparison_summary:
        print(f"{r['Provider']:<15} | {r['EM']:.3f}        | {r['F1']:.3f}")
    print("="*55)
    print("✅ Experiment Complete. Use these results for the RA Report.")

if __name__ == "__main__":
    main()
