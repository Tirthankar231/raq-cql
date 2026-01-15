# RAG + CQL Agent Lab

A hands-on laboratory project demonstrating powerful AI/LLM integration patterns with Apache Cassandra and document retrieval systems using Google's Gemini 2.0 Flash model.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Module 1: RAG Chatbot (Node.js)](#module-1-rag-chatbot-nodejs)
- [Module 2: CQL Agent (Node.js)](#module-2-cql-agent-nodejs)
- [Module 3: Agno Agent (Python)](#module-3-agno-agent-python)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [How It Works](#how-it-works)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

This repository contains three independent but complementary systems that showcase modern AI integration patterns:

| Module | Language | Purpose | Key Feature |
|--------|----------|---------|-------------|
| **RAG Chatbot** | Node.js | Question-answering over documents | Retrieval Augmented Generation |
| **CQL Agent** | Node.js | Natural language to database queries | Text-to-CQL conversion |
| **Agno Agent** | Python | Unified RAG + CQL agent | Agno framework with tool calling |

All modules leverage **Google Gemini 2.0 Flash** as the underlying Large Language Model (LLM) for intelligent text processing and generation.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Google Gemini 2.0 Flash (Shared LLM)                      │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼────────┐        ┌─────────▼─────────┐       ┌─────────▼─────────┐
│  RAG Chatbot   │        │    CQL Agent      │       │   Agno Agent      │
│   (Node.js)    │        │    (Node.js)      │       │    (Python)       │
├────────────────┤        ├───────────────────┤       ├───────────────────┤
│ • Doc Ingest   │        │ • Schema Aware    │       │ • RAG Tools       │
│ • Keyword Search│       │ • Query Gen       │       │ • CQL Tools       │
│ • Context Aug  │        │ • Query Exec      │       │ • Unified Agent   │
└───────┬────────┘        └─────────┬─────────┘       └─────────┬─────────┘
        │                           │                           │
┌───────▼────────┐        ┌─────────▼─────────┐       ┌─────────▼─────────┐
│  File Storage  │        │ Apache Cassandra  │       │  File + Cassandra │
│  (JSON/TXT)    │        │ (127.0.0.1:9042)  │       │  (Combined)       │
└────────────────┘        └───────────────────┘       └───────────────────┘
```

---

## Project Structure

```
rag-cql-lab/
│
├── README.md                    # This documentation file
│
├── rag-chatbot/                 # RAG-based Q&A chatbot (Node.js)
│   ├── package.json             # Node.js dependencies
│   ├── ingest.js                # Document chunking pipeline
│   ├── retrieve.js              # Keyword-based retrieval
│   ├── chat.js                  # Main chat interface
│   ├── data/
│   │   ├── docs.txt             # Source documents
│   │   └── chunks.json          # Processed chunks (generated)
│   └── .gitignore
│
├── cql-agent/                   # Natural language to CQL agent (Node.js)
│   ├── package.json             # Node.js dependencies
│   ├── schema.cql               # Cassandra schema definition
│   ├── agent.js                 # LLM-powered CQL generator
│   ├── db.js                    # Cassandra client setup
│   ├── run.js                   # Entry point & demo queries
│   └── .gitignore
│
└── agno-agent/                  # Unified RAG + CQL agent (Python)
    ├── requirements.txt         # Python dependencies
    ├── agent.py                 # Agent definitions with RAG & CQL tools
    ├── db.py                    # Cassandra client setup
    ├── knowledge.py             # Document loading & retrieval
    ├── main.py                  # Entry point & demo runner
    └── data/
        └── docs.txt             # Source documents
```

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Node.js** | Latest | Runtime environment (ES Modules) |
| **Python** | 3.10+ | Runtime for Agno agent |
| **Google Generative AI** | ^0.24.1 | Gemini 2.0 Flash LLM integration (Node.js) |
| **Agno** | Latest | Python AI agent framework with tool calling |
| **Apache Cassandra** | 4.x | Distributed NoSQL database |
| **Cassandra Driver** | ^4.8.0 | Node.js Cassandra client |
| **cassandra-driver** | Latest | Python Cassandra client |

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js** (v18 or higher recommended)
   ```bash
   node --version
   ```

2. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

3. **Python** (v3.10 or higher, for Agno Agent module)
   ```bash
   python --version
   ```

4. **Apache Cassandra** (for CQL Agent and Agno Agent modules)
   - Running locally on `127.0.0.1:9042`
   - Or use Docker:
     ```bash
     docker run -d --name cassandra -p 9042:9042 cassandra:latest
     ```

5. **Google Gemini API Key**
   - Obtain from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Tirthankar231/raq-cql.git
cd raq-cql/rag-cql-lab
```

### Set Up Environment Variable

```bash
# Linux/macOS
export GEMINI_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:GEMINI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your-api-key-here
```

### Install Dependencies

```bash
# For RAG Chatbot (Node.js)
cd rag-chatbot
npm install

# For CQL Agent (Node.js)
cd ../cql-agent
npm install

# For Agno Agent (Python)
cd ../agno-agent
pip install -r requirements.txt
```

---

## Module 1: RAG Chatbot (Node.js)

### What is RAG?

**Retrieval Augmented Generation (RAG)** is a technique that enhances LLM responses by:
1. Retrieving relevant context from a knowledge base
2. Augmenting the user's question with this context
3. Generating an informed response using the LLM

### Components

| File | Purpose |
|------|---------|
| `ingest.js` | Reads documents and splits them into searchable chunks |
| `retrieve.js` | Finds relevant chunks using keyword matching |
| `chat.js` | Combines retrieval with Gemini for intelligent Q&A |

### Data Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   docs.txt   │───▶│  ingest.js   │───▶│ chunks.json  │
│  (Raw Docs)  │    │  (Chunking)  │    │  (Indexed)   │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
┌──────────────┐    ┌──────────────┐    ┌──────▼───────┐
│   Response   │◀───│   chat.js    │◀───│ retrieve.js  │
│              │    │  (Gemini)    │    │  (Search)    │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Running the RAG Chatbot

```bash
cd rag-chatbot

# Step 1: Ingest documents (one-time setup)
npm run ingest

# Step 2: Run the chatbot
npm run chat
```

### Sample Output

```
Question: What is Cassandra?
Context: Apache Cassandra is a distributed NoSQL database...
Answer: Cassandra is a highly scalable, distributed NoSQL database
designed for handling large amounts of data across multiple servers...
```

---

## Module 2: CQL Agent (Node.js)

### What is the CQL Agent?

The CQL Agent converts **natural language questions** into valid **Cassandra Query Language (CQL)** statements, executes them against a Cassandra database, and returns formatted results.

### Components

| File | Purpose |
|------|---------|
| `schema.cql` | Defines database schema (keyspace, tables, sample data) |
| `db.js` | Initializes Cassandra client connection |
| `agent.js` | Uses Gemini to generate CQL from natural language |
| `run.js` | Entry point with demonstration queries |

### Database Schema

```sql
-- Keyspace
CREATE KEYSPACE agent_demo
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- Users Table
CREATE TABLE agent_demo.users (
    id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_date DATE
);

-- Sample Data
INSERT INTO agent_demo.users (id, name, email, created_date)
VALUES (uuid(), 'Rahul', 'rahul@example.com', '2026-01-15');
-- ... more sample users
```

### Data Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Natural    │───▶│  agent.js    │───▶│  CQL Query   │
│   Language   │    │  (Gemini)    │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                               │
┌──────────────┐    ┌──────────────┐    ┌──────▼───────┐
│   Results    │◀───│    db.js     │◀───│  Cassandra   │
│   (Table)    │    │  (Execute)   │    │  Database    │
└──────────────┘    └──────────────┘    └──────────────┘
```

### Running the CQL Agent

```bash
cd cql-agent

# Step 1: Start Cassandra (if not running)
# Using Docker:
docker run -d --name cassandra -p 9042:9042 cassandra:latest

# Wait for Cassandra to fully start (~30-60 seconds)
docker logs cassandra | grep "Starting listening"

# Step 2: Load the schema
cqlsh -f schema.cql

# Step 3: Run the agent
npm run run
```

### Sample Queries & Output

| Natural Language | Generated CQL |
|------------------|---------------|
| "Show all users" | `SELECT * FROM agent_demo.users;` |
| "Show users created on 2026-01-15" | `SELECT * FROM agent_demo.users WHERE created_date = '2026-01-15' ALLOW FILTERING;` |
| "List email and name of users" | `SELECT email, name FROM agent_demo.users;` |

### Sample Output

```
Question: Show all users

Generated CQL: SELECT * FROM agent_demo.users;

┌──────────────────────────────────────┬────────┬─────────────────────┬──────────────┐
│ id                                   │ name   │ email               │ created_date │
├──────────────────────────────────────┼────────┼─────────────────────┼──────────────┤
│ a1b2c3d4-e5f6-7890-abcd-ef1234567890 │ Rahul  │ rahul@example.com   │ 2026-01-15   │
│ b2c3d4e5-f6a7-8901-bcde-f12345678901 │ Anita  │ anita@example.com   │ 2026-01-14   │
│ c3d4e5f6-a7b8-9012-cdef-123456789012 │ Suresh │ suresh@example.com  │ 2026-01-15   │
└──────────────────────────────────────┴────────┴─────────────────────┴──────────────┘
```

---

## Module 3: Agno Agent (Python)

### What is the Agno Agent?

The Agno Agent is a **unified Python implementation** that combines both RAG and CQL capabilities into a single agent system using the **Agno framework**. It demonstrates how to build AI agents with tool calling capabilities.

### Why Agno?

| Feature | Benefit |
|---------|---------|
| **Tool Calling** | Native support for defining and registering custom tools |
| **Unified Agent** | Single agent can access both knowledge base and database |
| **Cleaner Code** | Declarative agent definition with instructions |
| **Built-in Features** | Markdown rendering, tool call visibility |

### Components

| File | Purpose |
|------|---------|
| `agent.py` | Defines RAG and CQL tools using Agno Toolkit, creates both agents |
| `db.py` | Cassandra client connection and query execution |
| `knowledge.py` | Document loading and keyword-based retrieval |
| `main.py` | Entry point that runs demos for both agents |

### Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Agno Agent Framework                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐              ┌─────────────────┐        │
│  │   RAG Chatbot   │              │    CQL Agent    │        │
│  │     Agent       │              │      Agent      │        │
│  └────────┬────────┘              └────────┬────────┘        │
│           │                                │                 │
│  ┌────────▼────────┐              ┌────────▼────────┐        │
│  │   RAGTools      │              │    CQLTools     │        │
│  │ ┌─────────────┐ │              │ ┌─────────────┐ │        │
│  │ │search_know- │ │              │ │run_cql_query│ │        │
│  │ │ledge_base() │ │              │ │()           │ │        │
│  │ └─────────────┘ │              │ └─────────────┘ │        │
│  └────────┬────────┘              └────────┬────────┘        │
│           │                                │                 │
└───────────┼────────────────────────────────┼─────────────────┘
            │                                │
   ┌────────▼────────┐              ┌────────▼────────┐
   │   knowledge.py  │              │      db.py      │
   │   (docs.txt)    │              │   (Cassandra)   │
   └─────────────────┘              └─────────────────┘
```

### Running the Agno Agent

```bash
cd agno-agent

# Step 1: Set up environment variable
export GEMINI_API_KEY="your-api-key-here"
# Or create a .env file:
echo 'GEMINI_API_KEY=your-api-key-here' > .env

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start Cassandra (if not running)
docker run -d --name cassandra -p 9042:9042 cassandra:latest

# Wait for Cassandra to fully start (~30-60 seconds)
docker logs cassandra | grep "Starting listening"

# Step 4: Load the schema (from cql-agent directory)
cqlsh -f ../cql-agent/schema.cql

# Step 5: Run the agent
python main.py
```

### Sample Output

```
Starting Agno Agent Lab...

============================================================
RAG CHATBOT DEMO
============================================================

────────────────────────────────────
Question: What is Cassandra?
────────────────────────────────────
🔧 Using tool: search_knowledge_base
Cassandra is a highly scalable, distributed NoSQL database...

============================================================
CQL AGENT DEMO
============================================================

────────────────────────────────────
Request: Show all users
────────────────────────────────────
🔧 Using tool: run_cql_query
Query: SELECT * FROM agent_demo.users;

| id | name | email | created_date |
|----|------|-------|--------------|
| ... | Rahul | rahul@example.com | 2026-01-15 |
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for LLM access |

### Setting Environment Variables

**Option 1: Export in terminal (temporary)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option 2: Create a .env file (recommended for development)**
```bash
# Create .env file in each module directory
echo 'GEMINI_API_KEY=your-api-key-here' > .env
```

> Note: Remember to add `.env` to your `.gitignore` to avoid committing secrets!

---

## Usage Examples

### RAG Chatbot Examples

```javascript
// Sample questions the chatbot can answer:
"What is Cassandra?"
"Explain RAG"
"What is CQL?"
```

### CQL Agent Examples

```javascript
// Sample natural language queries:
"Show all users"
"List users with their emails"
"Find users created on 2026-01-15"
"Show only names from the users table"
"Count all users"
```

### Agno Agent Examples

```python
# The Agno Agent can handle both RAG and CQL queries:

# RAG queries (knowledge base):
"What is Cassandra?"
"Explain RAG"
"What is CQL?"

# CQL queries (database):
"Show all users"
"Show users created on 2026-01-15"
"List email and name of users"
```

---

## How It Works

### RAG Chatbot - Under the Hood

1. **Ingestion Phase** (`ingest.js`)
   - Reads raw documents from `data/docs.txt`
   - Splits content into chunks (line-by-line)
   - Saves indexed chunks to `data/chunks.json`

2. **Retrieval Phase** (`retrieve.js`)
   - Extracts keywords from user query (filters stopwords)
   - Searches chunks for keyword matches
   - Returns all matching chunks as context

3. **Generation Phase** (`chat.js`)
   - Combines retrieved context with user question
   - Sends augmented prompt to Gemini
   - Returns LLM-generated answer

### CQL Agent - Under the Hood

1. **Schema Loading** (`agent.js`)
   - Reads `schema.cql` to understand database structure
   - Provides schema context to the LLM

2. **Query Generation** (`agent.js`)
   - Sends natural language + schema to Gemini
   - LLM generates valid CQL query
   - Cleans markdown formatting from response
   - Adds `ALLOW FILTERING` when needed

3. **Execution** (`run.js`)
   - Establishes Cassandra connection via `db.js`
   - Executes generated CQL query
   - Formats and displays results in table format

### Agno Agent - Under the Hood

1. **Tool Definition** (`agent.py`)
   - Defines `RAGTools` toolkit with `search_knowledge_base()` method
   - Defines `CQLTools` toolkit with `run_cql_query()` method
   - Tools are registered with the Agno framework for automatic invocation

2. **Agent Creation** (`agent.py`)
   - Creates two separate agents: RAG Chatbot and CQL Agent
   - Each agent has specific instructions and tools assigned
   - Uses Gemini 2.0 Flash model via Agno's Google integration

3. **Knowledge Management** (`knowledge.py`)
   - Loads documents on module import
   - Implements keyword-based retrieval (same logic as Node.js version)
   - Returns matching chunks as context

4. **Database Operations** (`db.py`)
   - Manages Cassandra connection lifecycle
   - Executes queries and returns results as dictionaries

5. **Execution** (`main.py`)
   - Runs demo queries for both agents sequentially
   - Handles connection setup and teardown
   - Uses `dotenv` for environment variable loading

---

## Future Improvements

### RAG Chatbot Enhancements
- [ ] Implement embedding-based semantic search (vector similarity)
- [ ] Add support for PDF and other document formats
- [ ] Implement conversation memory for multi-turn dialogues
- [ ] Add chunking strategies (sentence-level, paragraph-level)
- [ ] Integrate vector database (Pinecone, Weaviate, or Cassandra Vector)

### CQL Agent Enhancements
- [ ] Add query validation layer before execution
- [ ] Implement query history and caching
- [ ] Support for complex queries (JOINs via materialized views)
- [ ] Add natural language explanations of query results
- [ ] Support multiple tables and relationships

### Agno Agent Enhancements
- [ ] Add conversation memory for multi-turn dialogues
- [ ] Implement a unified agent that can use both RAG and CQL tools together
- [ ] Add streaming responses for better UX
- [ ] Implement agent chaining for complex workflows
- [ ] Add support for additional data sources (APIs, other databases)

### General Improvements
- [ ] Build web UI interface (React/Next.js)
- [ ] Add comprehensive error handling
- [ ] Implement logging and monitoring
- [ ] Add unit and integration tests
- [ ] Containerize with Docker Compose
- [ ] Add CI/CD pipeline

---

## Troubleshooting

### Common Issues

**1. "GEMINI_API_KEY not found"**
```bash
# Ensure the environment variable is set
echo $GEMINI_API_KEY

# If empty, set it:
export GEMINI_API_KEY="your-api-key"
```

**2. "Connection refused" (Cassandra)**
```bash
# Check if Cassandra is running
docker ps | grep cassandra

# If not running, start it:
docker start cassandra

# Wait 30-60 seconds for full initialization
```

**3. "Keyspace agent_demo does not exist"**
```bash
# Load the schema first
cd cql-agent
cqlsh -f schema.cql
```

**4. "Module not found" errors (Node.js)**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**5. "ModuleNotFoundError" (Python/Agno)**
```bash
# Ensure you're in the agno-agent directory
cd agno-agent

# Reinstall Python dependencies
pip install -r requirements.txt

# If using a virtual environment, ensure it's activated:
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows
```

**6. "Database not connected" (Agno Agent)**
```bash
# The Agno agent requires db.connect() to be called first
# This is handled automatically in main.py
# If running agent.py directly, ensure you call db.connect()
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Author

**Tirthankar**
- GitHub: [@Tirthankar231](https://github.com/Tirthankar231)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- Google Gemini team for the powerful LLM API
- Apache Cassandra community for the robust database
- The RAG research community for the retrieval-augmented generation paradigm
