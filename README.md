# AI-Prototype-Engineer-Practical-Assessment
📄 Enterprise AI Assistant – RAG-Based Prototype (Tasks 1–4)
Overview

This project implements an enterprise-ready AI assistant using Retrieval-Augmented Generation (RAG).
The system allows users to query documents (PDFs) and receive accurate, source-grounded answers, while addressing hallucination control, scalability, cost management, and monitoring.

The implementation is structured across four tasks, each demonstrating a critical AI prototyping capability.

Task Summary
Task	Focus
Task 1	LLM-powered Chat with PDF (RAG)
Task 2	Hallucination & Quality Control
Task 3	Rapid Iteration – Advanced Capability
Task 4	Enterprise AI System Architecture
TASK 1: LLM-Powered Chat with PDF (RAG)
Goal

Build a working prototype that allows users to:

Upload a PDF

Ask natural language questions

Receive answers grounded in the document content

Core Functionality

PDF ingestion and text extraction

Text chunking with overlap

Vector embeddings for semantic retrieval

FAISS-based vector storage

Context-aware answer generation using an LLM

Simple UI for interaction

RAG Workflow (Conceptual)
PDF → Text → Chunks → Embeddings → Vector DB
                                   ↓
User Query → Retriever → Context → LLM → Answer

Design Decisions
Why RAG?

Prevents the LLM from relying on pre-trained knowledge alone

Enables document-grounded answers

Improves accuracy and trust

Why Chunking?

LLMs have limited context windows

Chunking enables scalable retrieval

Overlap preserves context continuity

Trade-offs (Task 1)

Pros

High answer relevance

Fast semantic search

Modular and extensible

Cons

Requires embedding computation

Limited by context window size

Single-document focus in base version

TASK 2: Hallucination & Quality Control
Problem

LLMs tend to produce confident but incorrect answers, especially when:

Context is missing

Retrieval is weak

Prompts are unrestricted

In enterprise environments, this is unacceptable.

Causes of Hallucination (System-Specific)

Missing or insufficient retrieved context

LLM overconfidence bias

Weak semantic similarity signals

Lack of prompt constraints

Hallucination Control Strategy

A multi-layered guardrail approach is used.

High-Level Control Flow
User Query
   ↓
Retrieval Validation
   ↓
Context Confidence Check
   ↓
Prompt Constraints
   ↓
Answer or Safe Refusal

Implemented Guardrails
Guardrail 1: Source-Grounded Answers

The LLM can answer only using retrieved document content.

Guardrail 2: Confidence Threshold

If retrieved context is insufficient or weak, the system refuses to answer.

Guardrail 3: Explicit Fallback Responses

The system responds with:
“I don’t know based on the provided document.”

Examples of Improvement

Out-of-scope question
Before: Confident but incorrect answer
After: Clear refusal based on missing document evidence

Weak context
Before: Partial or speculative answer
After: “Not enough information in the document.”

Trade-offs (Task 2)

Pros

Strong reduction in hallucinations

Increased user trust

Transparent system behavior

Cons

More conservative answers

Some valid questions may be refused

Requires careful threshold tuning

TASK 3: Rapid Iteration – Advanced Capability
Chosen Capability: Multi-Document Reasoning
Description

The system is extended to reason across multiple documents simultaneously rather than a single PDF.

All document chunks are stored in a shared vector database, allowing retrieval across sources.

Why This Capability?

Reflects real enterprise knowledge systems

Demonstrates scalable RAG design

Enables synthesis across policies, reports, and documentation

Conceptual Flow
Multiple Documents
      ↓
Unified Vector Store
      ↓
Cross-Document Retrieval
      ↓
Combined Context
      ↓
LLM Answer

Trade-offs (Task 3)

Pros

Broader knowledge coverage

More realistic enterprise use

Enables complex reasoning

Cons

Higher retrieval cost

Increased token usage

No automatic conflict resolution between documents

Limitations

Context window limits still apply

No document prioritization

No long-term conversational memory

TASK 4: Enterprise AI System Architecture
Goal

Design a secure, scalable, and cost-controlled AI assistant for internal enterprise use.

High-Level Architecture Diagram (Textual)
Internal Data Sources
(PDFs, Wikis, Databases)
        ↓
Data Ingestion Layer
        ↓
Chunking & Preprocessing
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Retrieval Layer
        ↓
LLM Orchestration
        ↓
API / Chat Interface
        ↓
Monitoring & Cost Control

Component Breakdown
1. Data Ingestion

Validates documents

Attaches metadata (source, role, timestamp)

Supports scheduled updates

2. Chunking & Preprocessing

Normalizes text

Preserves context via overlap

Prepares data for retrieval

3. Embedding Generation

Converts text into semantic vectors

Computed once and reused

4. Vector Database

Enables fast similarity search

Supports metadata-based filtering

Scales horizontally in production

5. Retrieval Layer

Retrieves top relevant chunks

Applies confidence thresholds

Enforces access control

6. LLM Orchestration

Injects retrieved context

Applies prompt constraints

Controls temperature and model choice

7. Interface Layer

Web UI, chat, or internal tools

Authentication and authorization enforced

Cost Control Strategy

Pre-computed embeddings

Limited context window

Token usage tracking

Model tier selection

Optional caching and deduplication

Monitoring & Evaluation

Tracked metrics include:

Retrieval relevance

Hallucination rate

Latency

Token usage

Cost per query

User feedback

Logs support:

Debugging

Auditing

Compliance

Trade-offs (Task 4)

Pros

Enterprise-grade reliability

Strong hallucination control

Scalable and modular

Cons

Higher architectural complexity

Requires continuous tuning

Monitoring overhead

Overall Trade-offs (Across All Tasks)
Strengths

Accurate, document-grounded answers

Clear hallucination mitigation

Scalable RAG architecture

Enterprise-ready design thinking

Limitations

Dependent on embedding quality

Requires API usage cost

No automatic contradiction handling

Context window constraints remain
