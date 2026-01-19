import chromadb
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from loguru import logger

class SimpleRetrieverBasic:
    def __init__(self, embedding_model: str = 'all-MiniLM-L6-v2', bm25_weight: float = 0.5):
        logger.info('Initializing SentenceTransformer...')
        self.embedding_model = SentenceTransformer(embedding_model)
        self.bm25_weight = bm25_weight
        
        persist_dir = str(Path('./data/indices/chroma_db').absolute())
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection(name='hotpotqa_chunks')
        
        self.bm25_index = None
        self.chunk_texts = []
        self.chunk_metadata = []

    def build_indices(self, chunks: List[Dict]):
        # Alias for compatibility
        self.build_index(chunks)

    def build_index(self, chunks: List[Dict]):
        valid_chunks = [c for c in chunks if c.get('text') and len(c.get('text').strip()) > 0]
        self.chunk_texts = [c['text'] for c in valid_chunks]
        self.chunk_metadata = valid_chunks
        
        # Build BM25
        tokenized_docs = [doc.split() for doc in self.chunk_texts]
        self.bm25_index = BM25Okapi(tokenized_docs)
        
        # Batch processing to save RAM (Your Phase 2 Success Logic)
        logger.info(f'Indexing {len(self.chunk_texts)} chunks...')
        embeddings = self.embedding_model.encode(
            self.chunk_texts, 
            batch_size=4, 
            show_progress_bar=True
        ).tolist()
        
        ids = [str(c.get('chunk_id', f'c_{i}')) for i, c in enumerate(valid_chunks)]
        
        if self.collection.count() > 0:
            existing = self.collection.get()
            if existing['ids']:
                self.collection.delete(ids=existing['ids'])
            
        self.collection.add(documents=self.chunk_texts, embeddings=embeddings, ids=ids)
        logger.success(f'✅ Successfully indexed {len(self.chunk_texts)} chunks.')

    def retrieve(self, query: str, top_k: int = 5):
        if not self.chunk_texts: return []
        query_embedding = self.embedding_model.encode([query]).tolist()
        v_results = self.collection.query(query_embeddings=query_embedding, n_results=top_k)
        
        results = []
        if v_results['documents'] and len(v_results['documents'][0]) > 0:
            for i, doc in enumerate(v_results['documents'][0]):
                results.append({
                    'text': doc,
                    'score': float(1.0 - v_results['distances'][0][i]),
                    'chunk_id': v_results['ids'][0][i]
                })
        return results
