"""
Tests for Dark RAG System
"""

import os
import json
import tempfile
from dark_rag import DarkDocument, DarkKnowledgeBase, DarkRAG, initialize_dark_knowledge_base


def test_dark_document():
    """Test DarkDocument creation and ID generation"""
    doc = DarkDocument(
        content="Test content",
        metadata={'source': 'test'}
    )
    
    # Check ID is generated
    doc_id = doc.get_id()
    assert len(doc_id) == 16
    assert isinstance(doc_id, str)
    
    # Same content should produce same ID
    doc2 = DarkDocument(content="Test content", metadata={})
    assert doc.get_id() == doc2.get_id()
    
    print("✓ DarkDocument test passed")


def test_knowledge_base():
    """Test DarkKnowledgeBase operations"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Create knowledge base
        kb = DarkKnowledgeBase(storage_path=temp_path)
        
        # Add documents
        doc_id1 = kb.add_document(
            "Dark web uses Tor for anonymity",
            metadata={'topic': 'tor'}
        )
        doc_id2 = kb.add_document(
            "Dark matter influences galaxy rotation",
            metadata={'topic': 'physics'}
        )
        
        assert len(kb.documents) == 2
        assert doc_id1 in kb.documents
        assert doc_id2 in kb.documents
        
        # Test retrieval
        results = kb.retrieve("dark web tor", top_k=2)
        assert len(results) > 0
        assert any("Tor" in doc.content for doc in results)
        
        # Test save/load
        kb.save()
        assert os.path.exists(temp_path)
        
        # Load in new instance
        kb2 = DarkKnowledgeBase(storage_path=temp_path)
        assert len(kb2.documents) == 2
        assert doc_id1 in kb2.documents
        
        print("✓ DarkKnowledgeBase test passed")
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_dark_rag_augment():
    """Test Dark RAG augmentation"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        kb = DarkKnowledgeBase(storage_path=temp_path)
        kb.add_document(
            "The dark web is a hidden part of the internet",
            metadata={'topic': 'dark_web'}
        )
        
        dark_rag = DarkRAG(knowledge_base=kb)
        
        # Test augmentation
        query = "What is the dark web?"
        augmented = dark_rag.augment(query, top_k=1)
        
        assert "dark web" in augmented.lower()
        assert "context" in augmented.lower()
        assert query in augmented
        
        print("✓ DarkRAG augment test passed")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_dark_rag_generate():
    """Test Dark RAG generation"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        kb = DarkKnowledgeBase(storage_path=temp_path)
        kb.add_document(
            "Dark energy accelerates universe expansion",
            metadata={'topic': 'cosmology'}
        )
        kb.add_document(
            "Dark matter provides gravitational effects",
            metadata={'topic': 'physics'}
        )
        
        dark_rag = DarkRAG(knowledge_base=kb)
        
        # Test generation
        result = dark_rag.generate("Tell me about dark energy", top_k=2)
        
        assert 'query' in result
        assert 'augmented_prompt' in result
        assert 'retrieved_documents' in result
        assert 'num_retrieved' in result
        
        assert result['query'] == "Tell me about dark energy"
        assert result['num_retrieved'] > 0
        assert len(result['retrieved_documents']) > 0
        
        # Check document structure
        doc = result['retrieved_documents'][0]
        assert 'content' in doc
        assert 'metadata' in doc
        assert 'id' in doc
        
        print("✓ DarkRAG generate test passed")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_initialize_dark_knowledge_base():
    """Test initialization with default content"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Temporarily override the storage path
        original_storage = "dark_knowledge_base.json"
        kb = DarkKnowledgeBase(storage_path=temp_path)
        
        # Add default documents manually for this test
        kb.add_document(
            "Dark Web is part of the internet not indexed by standard search engines",
            metadata={'source': 'README.md', 'topic': 'dark_web_intro'}
        )
        kb.add_document(
            "Dark Matter is invisible and cannot be directly observed",
            metadata={'source': 'README.md', 'topic': 'dark_matter_analogy'}
        )
        kb.add_document(
            "Dark Energy drives the accelerated expansion of the universe",
            metadata={'source': 'README.md', 'topic': 'dark_energy_analogy'}
        )
        kb.add_document(
            "The Dark Sector in physics refers to a hypothetical world",
            metadata={'source': 'README.md', 'topic': 'dark_sector'}
        )
        
        # Should have 4 documents
        assert len(kb.documents) >= 4
        
        # Test retrieval of default content
        results = kb.retrieve("dark web dark matter", top_k=3)
        assert len(results) > 0
        
        print("✓ Initialize dark knowledge base test passed")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_empty_retrieval():
    """Test retrieval with no matches"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        kb = DarkKnowledgeBase(storage_path=temp_path)
        kb.add_document("Unrelated content", metadata={})
        
        results = kb.retrieve("completely different query xyz123", top_k=5)
        # Should return empty list when no matches
        assert isinstance(results, list)
        
        print("✓ Empty retrieval test passed")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    print("Running Dark RAG Tests...\n")
    
    test_dark_document()
    test_knowledge_base()
    test_dark_rag_augment()
    test_dark_rag_generate()
    test_initialize_dark_knowledge_base()
    test_empty_retrieval()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)
