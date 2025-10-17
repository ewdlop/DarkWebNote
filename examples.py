#!/usr/bin/env python3
"""
Example usage of Dark RAG System

This script demonstrates various use cases of the Dark RAG system.
"""

from dark_rag import DarkRAG, DarkKnowledgeBase, initialize_dark_knowledge_base


def example_1_basic_usage():
    """Example 1: Basic usage with pre-configured knowledge"""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    
    # Initialize with default dark web/dark matter knowledge
    kb = initialize_dark_knowledge_base()
    dark_rag = DarkRAG(knowledge_base=kb)
    
    # Query
    query = "Explain the dark sector concept"
    result = dark_rag.generate(query, top_k=2)
    
    print(f"\nQuery: {query}")
    print(f"\nRetrieved {result['num_retrieved']} relevant documents\n")
    
    for i, doc in enumerate(result['retrieved_documents'], 1):
        print(f"Document {i}:")
        print(f"  Topic: {doc['metadata'].get('topic', 'N/A')}")
        print(f"  Preview: {doc['content'][:80]}...")
        print()


def example_2_custom_knowledge():
    """Example 2: Adding custom knowledge"""
    print("\n" + "=" * 70)
    print("Example 2: Custom Knowledge Base")
    print("=" * 70)
    
    # Create custom knowledge base
    kb = DarkKnowledgeBase(storage_path="custom_kb.json")
    
    # Add custom documents
    kb.add_document(
        "The Tor network uses onion routing to provide anonymous communication. "
        "It encrypts data in multiple layers, like an onion, and routes it through "
        "a series of volunteer-operated servers.",
        metadata={'source': 'custom', 'topic': 'tor_technology'}
    )
    
    kb.add_document(
        "Bitcoin is a decentralized cryptocurrency often associated with dark web "
        "transactions due to its pseudonymous nature. However, all transactions are "
        "recorded on a public blockchain.",
        metadata={'source': 'custom', 'topic': 'cryptocurrency'}
    )
    
    kb.add_document(
        "Monero (XMR) is a privacy-focused cryptocurrency that uses ring signatures "
        "and stealth addresses to provide true anonymity, making it popular for "
        "private transactions.",
        metadata={'source': 'custom', 'topic': 'privacy_coins'}
    )
    
    kb.save()
    
    # Use in Dark RAG
    dark_rag = DarkRAG(knowledge_base=kb)
    
    query = "How do privacy cryptocurrencies work?"
    result = dark_rag.generate(query, top_k=2)
    
    print(f"\nQuery: {query}")
    print(f"\nRetrieved {result['num_retrieved']} relevant documents")
    print("\nAugmented Prompt (first 500 chars):")
    print(result['augmented_prompt'][:500] + "...")


def example_3_retrieval_only():
    """Example 3: Using just the retrieval component"""
    print("\n" + "=" * 70)
    print("Example 3: Retrieval Only (No Augmentation)")
    print("=" * 70)
    
    kb = initialize_dark_knowledge_base()
    
    # Direct retrieval
    query = "dark energy universe"
    docs = kb.retrieve(query, top_k=3)
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(docs)} relevant documents:\n")
    
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.content[:100]}...")
        print(f"   [Topic: {doc.metadata.get('topic', 'N/A')}]\n")


def example_4_knowledge_base_inspection():
    """Example 4: Inspecting the knowledge base"""
    print("\n" + "=" * 70)
    print("Example 4: Knowledge Base Inspection")
    print("=" * 70)
    
    kb = initialize_dark_knowledge_base()
    
    print(f"\nKnowledge Base Statistics:")
    print(f"  Total documents: {len(kb.documents)}")
    print(f"  Storage path: {kb.storage_path}")
    
    print("\n  Document topics:")
    topics = set()
    for doc in kb.documents.values():
        topic = doc.metadata.get('topic', 'unknown')
        topics.add(topic)
    
    for topic in sorted(topics):
        print(f"    - {topic}")


def example_5_multiple_queries():
    """Example 5: Running multiple queries"""
    print("\n" + "=" * 70)
    print("Example 5: Multiple Queries")
    print("=" * 70)
    
    kb = initialize_dark_knowledge_base()
    dark_rag = DarkRAG(knowledge_base=kb)
    
    queries = [
        "What is dark matter?",
        "How does the dark web work?",
        "What is the dark sector?"
    ]
    
    for query in queries:
        result = dark_rag.generate(query, top_k=1)
        print(f"\nQuery: {query}")
        print(f"Retrieved: {result['num_retrieved']} document(s)")
        if result['retrieved_documents']:
            doc = result['retrieved_documents'][0]
            print(f"Top result: {doc['content'][:80]}...")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "DARK RAG EXAMPLES" + " " * 31 + "║")
    print("╚" + "═" * 68 + "╝")
    
    example_1_basic_usage()
    example_2_custom_knowledge()
    example_3_retrieval_only()
    example_4_knowledge_base_inspection()
    example_5_multiple_queries()
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Read DARK_RAG.md for detailed documentation")
    print("  2. Customize the knowledge base for your use case")
    print("  3. Integrate with your preferred LLM for generation")
    print()


if __name__ == "__main__":
    main()
