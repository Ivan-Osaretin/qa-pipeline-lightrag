# GraphRAG Retriever: Sequence Based Pipeline Analysis

This document outlines my four-stage retrieval process implemented in the LightRAG pipeline.

## Stage 1: Dual-Stream Candidate Identification
- **Lexical Signal Best Match 25 algorithm (BM25):** This system utilizes the BM25 ranking algorithm to score document chunks slash paragraphs based on keyword frequency and rarity.

- **Semantic Signal (Vector):** The query is embedded utilzing `all-MiniLM-L6-v2`(a highly efficient transformer model developed for generating sentence embeddings. It excels in natural language processing (nlp) tasks by mapping sentences and paragraphs to a 384-dimensional dense vector space).

Cosine Similarity search in ChromaDB works by converting text (or other data) into numerical vectors (embeddings) that capture meaning.
ChromaDB's Role: A vector database like Chroma stores and indexes these high-dimensional vectors, optimized for fast lookups.
Cosine Similarity Metric: It calculates the cosine of the angle between the query vector and each document vector.
Semantic Proximity: A cosine value of 1 means identical direction (highly similar), 0 means orthogonal (unrelated), and -1 means opposite.
Finding Context: Chroma returns vectors (and their associated text) closest to the query vector in the vector space, providing semantically relevant results. 
Key Advantages:
Meaning Over Words: Understands "cat" and "dog" are similar because they are both pets, not just because they're spelled differently.
Efficient: Computes similarity based on direction, not magnitude, making it great for text. 
In Practice (ChromaDB):
A User provides a query, Chroma converts it to a vector, then searches its collection for vectors with the highest cosine similarity score (closest angle) to find related data for tasks like RAG. 

 So Cosine Similarity search programmable technique, is performed within the ChromaDataBase to find context with semantic proximity.

 Terms: Indexing Time (putting books on the shelf from the data stored in the ChromaDB) Query Time (looking for a book from the data stored in the ChromaDB)

 Top-K is a Selection Criteria set of algorithms to aid me in determining and coming to the conclusion that:

 K is a number (in my code, I set to top_k=3).
 The Logic: I run two mathematical "contests":
 Lexical Contest (BM25): Which 3 paragraphs have the most exact word-matches?
 Semantic Contest (Vector Search): Which 3 paragraphs have the most similar mathematical meaning (using Cosine Similarity)?

The Result: The "Top-K" are the winners of these contests.

- **Result:** Selection logic of Top-K "Anchor Chunks."

## Stage 2: Entity Grounding (Graph Entry)
- **Signal:** Direct keyword overlap between query tokens and Knowledge Graph entities.
- **Action:** The system maps the query to specific "Entity Nodes" (e.g., PERSON, ORG) within the 1,929-node NetworkX graph.
- **Purpose:** Establishing a starting point for structural reasoning.

## Stage 3: Multi-Hop Subgraph Expansion
- **Algorithm:** Depth-1 Adjacency Traversal.
- **Logic:** For every grounded entity, the engine retrieves all immediate neighbors connected by `mentions` or `co_occurs` edges.
- **Innovation:** This associative retrieval allows the system to resolve multi-hop dependencies by bridging information across disparate documents that lack direct semantic similarity.

## Stage 4: Context Assembly & Fusion
- **Technical Step:** Integration of unstructured search results and structured graph context.
- **Deduplication:** A Python `set()` logic is applied to the combined context to maximize the efficiency of the LLM context window.
- **Output:** A structured prompt partitioned into "Direct Context" and "Related Knowledge" for the Llama-3.3/Command R+ inference engine.