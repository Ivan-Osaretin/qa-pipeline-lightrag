import json
import time
from tqdm import tqdm
from lightrag_pipeline import LightRAGPipeline
from loguru import logger

def main():
    # 1. Loads Data
    with open('data/processed/dev_subset_100.json', 'r') as f:
        examples = json.load(f)['examples']

    # 2. Initializes The Pipeline
    # (This builds the retriever and loads my 1,929-node graph locally)
    pipeline = LightRAGPipeline("data/indices/complete_graph.pkl", examples)

    final_delivery_data = []
    
    print("\n" + "!"*60)
    print("PRODUCING FINAL 100-QUESTION AUDIT FILE")
    print("Strategy: 12-second delay per query to wisely bypass API limits.")
    print("Estimated completion time: 20 minutes.")
    print("!"*60 + "\n")

    # 3. The Loop
    for ex in tqdm(examples, desc="📦 Finalizing Delivery"):
        try:
            # Mandatoy delay to protect my free API credits
            time.sleep(12) 
            
            # This captures: Answer + Entities + Context
            details = pipeline.answer_question_detailed(ex['question'])
            
            final_delivery_data.append({
                "qid": ex['_id'],
                "question": ex['question'],
                "gold_answer": ex['answer'],
                "lightrag_answer": details['final_answer'],
                "intermediate_artifacts": {
                    "retrieved_entities": details['retrieved_entities'],
                    "retrieved_context_chunks": details['retrieved_context'],
                    "graph_augmented_context": details['graph_context_provided']
                }
            })
        except Exception as e:
            logger.error(f"Error on QID {ex['_id']}: {e}")
            # If it fails, save a placeholder so the file isn't empty
            final_delivery_data.append({"qid": ex['_id'], "error": str(e)})

    # 4. Saves Final JSON for Havva
    output_path = 'data/indices/detailed_outputs_100.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_delivery_data, f, indent=2)
    
    logger.success(f"✅ MISSION ACCOMPLISHED. Deliverable created: {output_path}")

if __name__ == "__main__":
    main()