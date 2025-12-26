"""
PHASE 2 - ENTITY EXTRACTOR
First component: Extract entities from HotpotQA chunks
"""
import spacy
from typing import List, Dict, Any, Set
from dataclasses import dataclass
from loguru import logger
import json

@dataclass
class ExtractedEntity:
    text: str
    label: str  # PERSON, ORG, GPE, etc.
    start_char: int
    end_char: int
    chunk_id: str
    
class EntityExtractor:
    """Extract entities from text chunks using SpaCy"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        logger.info(f"Initializing EntityExtractor with {model_name}")
        self.nlp = spacy.load(model_name)
        self.entity_types = {"PERSON", "ORG", "GPE", "DATE", "EVENT", "WORK_OF_ART"}
    
    def extract_from_chunk(self, chunk: Dict) -> List[ExtractedEntity]:
        """Extract entities from a single chunk"""
        chunk_id = chunk.get("chunk_id", "unknown")
        text = chunk.get("text", "")
        
        if not text:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in self.entity_types:
                entities.append(ExtractedEntity(
                    text=ent.text,
                    label=ent.label_,
                    start_char=ent.start_char,
                    end_char=ent.end_char,
                    chunk_id=chunk_id
                ))
        
        logger.debug(f"Extracted {len(entities)} entities from chunk {chunk_id}")
        return entities
    
    def extract_from_chunks(self, chunks: List[Dict]) -> Dict[str, List[ExtractedEntity]]:
        """Extract entities from multiple chunks"""
        results = {}
        
        logger.info(f"Extracting entities from {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            if i % 10 == 0:
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            
            chunk_id = chunk.get("chunk_id", f"chunk_{i}")
            entities = self.extract_from_chunk(chunk)
            
            if entities:
                results[chunk_id] = entities
        
        logger.info(f"Total entities extracted: {sum(len(v) for v in results.values())}")
        return results
    
    def save_entities(self, entities: Dict[str, List[ExtractedEntity]], path: str):
        """Save extracted entities to JSON file"""
        serializable = {}
        for chunk_id, entity_list in entities.items():
            serializable[chunk_id] = [
                {
                    "text": e.text,
                    "label": e.label,
                    "start_char": e.start_char,
                    "end_char": e.end_char
                }
                for e in entity_list
            ]
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2)
        
        logger.info(f"Saved entities to {path}")

def test_extractor():
    """Test the entity extractor"""
    print("=" * 60)
    print("🧪 TESTING ENTITY EXTRACTOR")
    print("=" * 60)
    
    extractor = EntityExtractor()
    
    # Tests with sample HotpotQA-like data
    test_chunks = [
        {
            "chunk_id": "test_1",
            "text": "Askold Khovanskii is a mathematician who worked on algebraic geometry at Moscow State University."
        },
        {
            "chunk_id": "test_2",
            "text": "The Consul and Arlecchino are both musical works composed in the 20th century."
        }
    ]
    
    entities = extractor.extract_from_chunks(test_chunks)
    
    for chunk_id, entity_list in entities.items():
        print(f"\n📄 Chunk: {chunk_id}")
        for entity in entity_list[:3]:  # Show first 3
            print(f"   • {entity.text} ({entity.label})")
    
    print("\n✅ Entity extractor test completed!")
    return entities

if __name__ == "__main__":
    test_extractor()