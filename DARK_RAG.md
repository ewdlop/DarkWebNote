# Dark RAG (Retrieval-Augmented Generation)

## Overview

Dark RAG is a Retrieval-Augmented Generation system themed around the philosophical concepts of the Dark Web, Dark Matter, and Dark Energy. Like dark matter that influences visible matter through gravity while remaining invisible, Dark RAG influences text generation through hidden knowledge retrieval.

## Concept

The Dark RAG system embodies the following metaphors:

- **Dark Knowledge Base** ≈ **Dark Matter**: Hidden knowledge that influences responses without being directly visible
- **Retrieval Process** ≈ **Gravitational Effects**: The way hidden knowledge pulls and shapes generated content
- **Augmented Generation** ≈ **Dark Energy**: The driving force that accelerates and enhances information flow

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Query                       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              Dark RAG System                        │
│  ┌─────────────────────────────────────────────┐   │
│  │   1. Query Processing                       │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   2. Knowledge Retrieval                    │   │
│  │      (from Dark Knowledge Base)             │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   3. Context Augmentation                   │   │
│  │      (merge query + retrieved docs)         │   │
│  └─────────────────┬───────────────────────────┘   │
│                    │                                │
│                    ▼                                │
│  ┌─────────────────────────────────────────────┐   │
│  │   4. Generation (Ready for LLM)             │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            Augmented Prompt + Context               │
└─────────────────────────────────────────────────────┘
```

## Components

### 1. DarkDocument

Represents a document in the dark knowledge base.

```python
@dataclass
class DarkDocument:
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
```

### 2. DarkKnowledgeBase

Stores and manages the hidden knowledge repository.

**Key Methods:**
- `add_document(content, metadata)`: Add a document to the knowledge base
- `retrieve(query, top_k)`: Retrieve relevant documents based on a query
- `save()`: Persist knowledge base to disk
- `load()`: Load knowledge base from disk

### 3. DarkRAG

The main RAG system that combines retrieval and augmentation.

**Key Methods:**
- `augment(query, top_k)`: Augment a query with retrieved context
- `generate(query, top_k)`: Generate a complete RAG response with metadata

## Usage

### Basic Usage

```python
from dark_rag import DarkRAG, initialize_dark_knowledge_base

# Initialize with pre-configured dark web knowledge
kb = initialize_dark_knowledge_base()
dark_rag = DarkRAG(knowledge_base=kb)

# Query the system
result = dark_rag.generate("What is the relationship between dark web and dark matter?")

print(f"Retrieved {result['num_retrieved']} documents")
print(f"Augmented prompt:\n{result['augmented_prompt']}")
```

### Adding Custom Knowledge

```python
from dark_rag import DarkKnowledgeBase, DarkRAG

# Create a custom knowledge base
kb = DarkKnowledgeBase(storage_path="my_dark_kb.json")

# Add documents
kb.add_document(
    "Tor (The Onion Router) is a software that enables anonymous communication.",
    metadata={'source': 'custom', 'topic': 'tor'}
)

kb.add_document(
    "Cryptocurrency like Bitcoin is often used in dark web marketplaces.",
    metadata={'source': 'custom', 'topic': 'cryptocurrency'}
)

# Save the knowledge base
kb.save()

# Use in Dark RAG
dark_rag = DarkRAG(knowledge_base=kb)
result = dark_rag.generate("How does Tor work?", top_k=2)
```

### Retrieval Only

```python
from dark_rag import DarkKnowledgeBase

kb = DarkKnowledgeBase()
kb.load()

# Retrieve relevant documents
docs = kb.retrieve("dark energy universe", top_k=3)

for doc in docs:
    print(f"Content: {doc.content}")
    print(f"Metadata: {doc.metadata}")
```

## Features

### Current Features

1. **Document Storage**: JSON-based persistent storage for the knowledge base
2. **Simple Retrieval**: Keyword-based document retrieval
3. **Context Augmentation**: Automatic prompt augmentation with retrieved context
4. **Metadata Support**: Rich metadata for each document
5. **Content Hashing**: Unique document IDs based on content

### Future Enhancements

1. **Vector Embeddings**: Integration with sentence transformers for semantic search
2. **Advanced Retrieval**: Support for vector similarity search (FAISS, ChromaDB)
3. **Hybrid Search**: Combine keyword and semantic search
4. **Document Chunking**: Smart document splitting for better retrieval
5. **Caching**: LRU cache for frequently retrieved documents
6. **Multi-modal Support**: Support for images and other media types

## Example Output

```
Query: What is the relationship between dark web and dark matter?

Retrieved 3 documents:

Document 1:
  ID: a3f2c1d4e5b6f789
  Topic: dark_matter_analogy
  Content: Dark Matter is invisible and cannot be directly observed...

Document 2:
  ID: b7e8d9c0a1f2e3d4
  Topic: dark_web_intro
  Content: Dark Web is part of the internet not indexed by standard...

Document 3:
  ID: c9f0e1d2b3a4c5d6
  Topic: dark_sector
  Content: The Dark Sector in physics refers to a hypothetical world...

Augmented Prompt:
Based on the following context from the dark knowledge base:

[Context 1]
Dark Matter is invisible and cannot be directly observed, but can be confirmed 
through gravitational effects like galaxy rotation curves and gravitational lensing. 
Similarly, the dark web cannot be directly 'seen' but we can know it exists through 
indirect evidence.

[Context 2]
Dark Web is part of the internet not indexed by standard search engines, 
accessible only through specific protocols like Tor. It represents invisible 
but existing parts of the information world.

[Context 3]
The Dark Sector in physics refers to a hypothetical world composed of dark matter, 
dark energy, or other unknown particles that exist in parallel with the visible 
matter world of the Standard Model. The dark web is like the 'dark sector of the 
information world' with its own rules, currencies (Bitcoin, Monero), communities, 
and markets.

Query: What is the relationship between dark web and dark matter?

Please provide a response informed by the context above.
```

## Philosophy

Dark RAG embodies the concept that knowledge, like dark matter, can be invisible yet influential. The system retrieves hidden context that shapes the generation process without being explicitly visible in the final output - much like how dark matter shapes galaxies through gravity without being seen.

## Integration with LLMs

Dark RAG prepares augmented prompts that can be sent to any LLM:

```python
# Get augmented prompt
result = dark_rag.generate("your query here")

# Send to OpenAI, Claude, or any other LLM
import openai
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": result['augmented_prompt']}
    ]
)
```

## File Structure

```
DarkWebNote/
├── dark_rag.py                 # Main Dark RAG implementation
├── DARK_RAG.md                 # This documentation
├── requirements.txt            # Python dependencies
├── dark_knowledge_base.json    # Persisted knowledge base (generated)
└── README.md                   # Repository README
```

## License

This implementation follows the repository's license.
