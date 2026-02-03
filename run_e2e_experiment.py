"""
END-TO-END EXPERIMENT RUNNER
"""
import json
from tqdm import tqdm
from lightrag_pipeline import LightRAGPipeline
from phase2.evaluation.rag_evaluator import RAGEvaluator
from loguru import logger

def run_experiment():
    # 1. Load Data
    with open('data/processed/dev_subset_100.json', 'r') as f:
        examples = json.load(f)['examples']

    # 2. Initializes Unified Pipeline
    pipeline = LightRAGPipeline("data/indices/complete_graph.pkl", examples)

    # 3. Run all 100 questions
    results = []
    logger.info("🚀 Running end-to-end experiment on 100 cases...")
    for ex in tqdm(examples):
        answer = pipeline.answer_question(ex['question'])
        results.append({
            "id": ex['_id'],
            "question": ex['question'],
            "gold_answer": ex['answer'],
            "predicted_answer": answer
        })

    # 4. Final Evaluation
    evaluator = RAGEvaluator()
    preds = [r['predicted_answer'] for r in results]
    golds = [r['gold_answer'] for r in results]
    metrics = evaluator.evaluate_batch(preds, golds)
    
    # 5. Output
    print("\n" + "="*30)
    print("END-TO-END EXPERIMENT RESULTS")
    print("="*30)
    print(f"Exact Match: {metrics['exact_match']['mean']:.3f}")
    print(f"F1 Score: {metrics['f1_score']['mean']:.3f}")
    print("="*30)

if __name__ == "__main__":
    run_experiment()