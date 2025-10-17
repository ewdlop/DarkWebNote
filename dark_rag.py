"""
Dark RAG - Retrieval-Augmented Generation System
Themed around the Dark Web metaphor of hidden but influential knowledge
"""

import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib


@dataclass
class DarkDocument:
    """Represents a document in the dark knowledge base"""
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    
    def get_id(self) -> str:
        """Generate a unique ID based on content hash"""
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]


class DarkKnowledgeBase:
    """
    Dark Knowledge Base - stores hidden knowledge like dark matter
    Invisible to surface searches but influential through retrieval
    """
    
    def __init__(self, storage_path: str = "dark_knowledge_base.json"):
        self.storage_path = storage_path
        self.documents: Dict[str, DarkDocument] = {}
        self.load()
    
    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a document to the dark knowledge base"""
        if metadata is None:
            metadata = {}
        
        doc = DarkDocument(content=content, metadata=metadata)
        doc_id = doc.get_id()
        self.documents[doc_id] = doc
        return doc_id
    
    def retrieve(self, query: str, top_k: int = 5) -> List[DarkDocument]:
        """
        Retrieve relevant documents based on query
        Simple keyword-based retrieval (can be enhanced with embeddings)
        """
        query_lower = query.lower()
        scored_docs = []
        
        for doc_id, doc in self.documents.items():
            # Simple scoring based on keyword overlap
            content_lower = doc.content.lower()
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]
    
    def save(self):
        """Persist the knowledge base to disk"""
        data = {
            doc_id: {
                'content': doc.content,
                'metadata': doc.metadata
            }
            for doc_id, doc in self.documents.items()
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Load the knowledge base from disk"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for doc_id, doc_data in data.items():
                    doc = DarkDocument(
                        content=doc_data['content'],
                        metadata=doc_data.get('metadata', {})
                    )
                    self.documents[doc_id] = doc
            except Exception as e:
                print(f"Error loading knowledge base: {e}")


class DarkRAG:
    """
    Dark Retrieval-Augmented Generation
    
    Like dark matter influences visible matter through gravity,
    this system influences generation through hidden knowledge retrieval
    """
    
    def __init__(self, knowledge_base: Optional[DarkKnowledgeBase] = None):
        self.knowledge_base = knowledge_base or DarkKnowledgeBase()
    
    def augment(self, query: str, top_k: int = 3) -> str:
        """
        Augment a query with retrieved context from the dark knowledge base
        
        Args:
            query: The input query
            top_k: Number of documents to retrieve
            
        Returns:
            Augmented prompt with retrieved context
        """
        retrieved_docs = self.knowledge_base.retrieve(query, top_k=top_k)
        
        if not retrieved_docs:
            return query
        
        # Build context from retrieved documents
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"[Context {i}]\n{doc.content}\n")
        
        context = "\n".join(context_parts)
        
        # Create augmented prompt
        augmented_prompt = f"""Based on the following context from the dark knowledge base:

{context}

Query: {query}

Please provide a response informed by the context above."""
        
        return augmented_prompt
    
    def generate(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Generate a response with RAG
        
        Returns both the augmented prompt and retrieved documents
        """
        retrieved_docs = self.knowledge_base.retrieve(query, top_k=top_k)
        augmented_prompt = self.augment(query, top_k=top_k)
        
        return {
            'query': query,
            'augmented_prompt': augmented_prompt,
            'retrieved_documents': [
                {
                    'content': doc.content,
                    'metadata': doc.metadata,
                    'id': doc.get_id()
                }
                for doc in retrieved_docs
            ],
            'num_retrieved': len(retrieved_docs)
        }


def initialize_dark_knowledge_base() -> DarkKnowledgeBase:
    """Initialize the dark knowledge base with default dark web content"""
    kb = DarkKnowledgeBase()
    
    # Add content from the README about dark web and dark matter
    kb.add_document(
        "Dark Web is part of the internet not indexed by standard search engines, "
        "accessible only through specific protocols like Tor. It represents invisible "
        "but existing parts of the information world.",
        metadata={'source': 'README.md', 'topic': 'dark_web_intro'}
    )
    
    kb.add_document(
        "Dark Matter is invisible and cannot be directly observed, but can be confirmed "
        "through gravitational effects like galaxy rotation curves and gravitational lensing. "
        "Similarly, the dark web cannot be directly 'seen' but we can know it exists through "
        "indirect evidence.",
        metadata={'source': 'README.md', 'topic': 'dark_matter_analogy'}
    )
    
    kb.add_document(
        "Dark Energy drives the accelerated expansion of the universe. In metaphor to the "
        "network world, the dark web acts as a 'driving force' that pushes human information "
        "exchange and economic activities toward privacy and decentralization.",
        metadata={'source': 'README.md', 'topic': 'dark_energy_analogy'}
    )
    
    kb.add_document(
        "The Dark Sector in physics refers to a hypothetical world composed of dark matter, "
        "dark energy, or other unknown particles that exist in parallel with the visible "
        "matter world of the Standard Model. The dark web is like the 'dark sector of the "
        "information world' with its own rules, currencies (Bitcoin, Monero), communities, "
        "and markets.",
        metadata={'source': 'README.md', 'topic': 'dark_sector'}
    )
    
    kb.save()
    return kb


if __name__ == "__main__":
    # Example usage
    print("=== Dark RAG System ===\n")
    
    # Initialize with dark web themed knowledge
    kb = initialize_dark_knowledge_base()
    dark_rag = DarkRAG(knowledge_base=kb)
    
    # Test query
    test_query = "What is the relationship between dark web and dark matter?"
    
    print(f"Query: {test_query}\n")
    result = dark_rag.generate(test_query, top_k=3)
    
    print(f"\nRetrieved {result['num_retrieved']} documents:\n")
    for i, doc in enumerate(result['retrieved_documents'], 1):
        print(f"Document {i}:")
        print(f"  ID: {doc['id']}")
        print(f"  Topic: {doc['metadata'].get('topic', 'N/A')}")
        print(f"  Content: {doc['content'][:100]}...\n")
    
    print("=" * 60)
    print("\nAugmented Prompt:\n")
    print(result['augmented_prompt'])
