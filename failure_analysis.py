"""
PHASE 4 - FAILURE ANALYSIS SCRIPT (FIXED)
Generates the specific 10-case debug table requested by Havva.
"""
import json
import os
import sys
from pathlib import Path

# --- 1. PATH CONFIGURATION ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    # Use the exact imports that worked for your Phase 3 run
    from phase2.retrieval.dual_retriever import SimpleRetrieverBasic as DualLevelRetriever
    from phase2.evaluation.rag_evaluator import RAGEvaluator
    print("✅ All modules successfully linked.")
except ImportError as e:
    print(f"❌ LINKAGE ERROR: {e}")
    print("Ensure this script is located in the root 'qa-pipeline-lightrag' folder.")
    sys.exit(1)

def run_analysis():
    print("🔍 Loading data for Failure Analysis...")

    # 1. Load the Predictions and Original Data
    try:
        with open('data/indices/final_predictions_phase3.json', 'r', encoding='utf-8') as f:
            predictions = json.load(f)
        with open('data/processed/dev_subset_100.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            examples = data['examples']
    except FileNotFoundError as e:
        print(f"❌ Missing data files: {e}")
        return

    # 2. Setup Retriever (Singular 'build_index' as per your Phase 3 logs)
    retriever = DualLevelRetriever()
    
    # --- FIXED LINE BELOW ---
    chunks = []
    for ex in examples:
        context_text = " ".join([f"{t}: {' '.join(s)}" for t, s in ex['context']])
        chunks.append({'chunk_id': ex['_id'], 'text': context_text})
    
    # Try singular or plural based on what your module supports
    try:
        retriever.build_index(chunks)
    except AttributeError:
        retriever.build_indices(chunks)

    # 3. Filter for 10 "Failed" cases (EM = 0)
    failed_cases = []
    for p in predictions:
        gold = str(p['gold_answer']).lower().strip()
        pred = str(p['predicted_answer']).lower().strip()
        
        if gold != pred:
            failed_cases.append(p)
        
        if len(failed_cases) >= 10:
            break

    # 4. Print Table Data
    print("\n" + "="*120)
    print(f"{'QID':<25} | {'GOLD':<15} | {'ROOT CAUSE':<25}")
    print("-" * 120)

    for case in failed_cases:
        qid = case['id']
        gold = case['gold_answer']
        pred = case['predicted_answer'].strip().replace("\n", " ")
        
        # Check if retriever found the info
        retrieved = retriever.retrieve(case['question'], top_k=2)
        context_blob = " ".join([r['text'] for r in retrieved]).lower()

        # Determine Root Cause
        if gold.lower() in pred.lower():
            root_cause = "Metric Sensitivity (Verbosity)"
        elif gold.lower() in context_blob:
            root_cause = "LLM Extraction Error"
        else:
            root_cause = "Retrieval/Graph Miss"

        print(f"{qid:<25} | {gold:<15} | {root_cause:<25}")
        print(f"  > Question: {case['question'][:100]}...")
        print(f"  > AI Answer: {pred[:100]}...")
        
        snippets = " | ".join([r['text'][:60] + "..." for r in retrieved])
        print(f"  > Top-k Context: {snippets}")
        print("-" * 120)

    print("\n✅ Analysis Complete. Copy this data into Havva's table.")

if __name__ == "__main__":
    run_analysis()