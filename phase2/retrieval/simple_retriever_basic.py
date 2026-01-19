# 2. Create simple_retriever_basic.py
$retrieverCode = @"
"""
ULTRA-SIMPLE Retriever - Just keyword matching
"""
class SimpleRetrieverBasic:
    def __init__(self):
        self.chunks = []
    
    def build_index(self, chunks):
        """Just store chunks"""
        self.chunks = chunks
        print(f"Stored {len(chunks)} chunks for retrieval")
    
    def retrieve(self, query, top_k=3):
        """Simple keyword search"""
        results = []
        query_lower = query.lower()
        
        for chunk in self.chunks[:20]:  # Search first 20
            text = chunk.get('text', '').lower()
            if query_lower in text:
                results.append({
                    'text': chunk.get('text', '')[:100],
                    'score': 1.0
                })
        
        return results[:top_k]
"@

$retrieverCode | Out-File -FilePath "phase2/retrieval/simple_retriever_basic.py" -Encoding utf8
Write-Host "✅ Created phase2/retrieval/simple_retriever_basic.py" -ForegroundColor Green