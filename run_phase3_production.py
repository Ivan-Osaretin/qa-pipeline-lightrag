import json
import sys
import os
from pathlib import Path
from tqdm import tqdm
from loguru import logger
from dotenv import load_dotenv

load_dotenv() # Finds .env in root

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

try:
    # IMPORT ALIGNMENT: Point exactly to the class discovered in your logs
    from phase2.retrieval.dual_retriever import SimpleRetrieverBasic as DualLevelRetriever
    from phase3.llm_integration.groq_client import GroqClient
    from phase3.reasoning.reasoning_engine import ReasoningEngine
    from phase3.evaluation.final_evaluator import FinalEvaluator
    from phase2.evaluation.rag_evaluator import RAGEvaluator
    logger.info("✅ All modules successfully linked.")
except Exception as e:
    logger.error(f"❌ LINKAGE ERROR: {e}")
    sys.exit(1)

def main():
    logger.info('🚀 Phase 3 PRODUCTION START')
    
    if not os.getenv('GROQ_API_KEY'):
        logger.error("❌ GROQ_API_KEY missing in .env!")
        return

    llm = GroqClient()
    retriever = DualLevelRetriever()
    
    with open('data/processed/dev_subset_100.json', 'r') as f:
        data = json.load(f)
        examples = data['examples']
    
    chunks = [{'chunk_id': ex['_id'], 'text': " ".join([f"{t}: {' '.join(s)}" for t, s in ex['context']])} for ex in examples]
    
    logger.info("🏗️ Building Search Indices...")
    retriever.build_indices(chunks)
    
    engine = ReasoningEngine('data/indices/complete_graph.pkl', retriever)
    results = []
    
    for ex in tqdm(examples, desc='🤖 Querying Llama-3.3'):
        answer = engine.run_rag_pipeline(ex['question'], llm)
        results.append({'id': ex['_id'], 'question': ex['question'], 'gold_answer': ex['answer'], 'predicted_answer': answer})
    
    out_path = 'data/indices/final_predictions_phase3.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

    eval_tool = FinalEvaluator()
    metrics = eval_tool.run_final_audit(out_path)
    
    report_path = 'reports/PHASE3_FINAL_REPORT.md'
    report_content = RAGEvaluator().generate_report(metrics, model_name='LightRAG (Groq/Llama-3.3)')
    with open(report_path, 'w') as f:
        f.write(report_content)
        
    logger.success(f'🎉 PHASE 3 CONCLUDED. Final Report: {report_path}')

if __name__ == '__main__':
    main()
