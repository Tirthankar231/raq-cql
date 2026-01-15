# RAG + CQL Agent Lab

A hands-on laboratory project demonstrating two powerful AI/LLM integration patterns with Apache Cassandra and document retrieval systems using Google's Gemini 2.0 Flash model.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Module 1: RAG Chatbot](#module-1-rag-chatbot)
- [Module 2: CQL Agent](#module-2-cql-agent)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [How It Works](#how-it-works)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

This repository contains two independent but complementary systems that showcase modern AI integration patterns:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| **RAG Chatbot** | Question-answering over documents | Retrieval Augmented Generation |
| **CQL Agent** | Natural language to database queries | Text-to-CQL conversion |

Both modules leverage **Google Gemini 2.0 Flash** as the underlying Large Language Model (LLM) for intelligent text processing and generation.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Google Gemini 2.0 Flash (Shared LLM)           │
└─────────────────────────────┬───────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
     ┌────────▼─────────┐          ┌──────────▼──────────┐
     │   RAG Chatbot    │          │     CQL Agent       │
     ├──────────────────┤          ├─────────────────────┤
     │ • Document Ingest│          │ • Schema Awareness  │
     │ • Keyword Search │          │ • Query Generation  │
     │ • Context Augment│          │ • Query Execution   │
     └────────┬─────────┘          └──────────┬──────────┘
              │                               │
     ┌────────▼─────────┐          ┌──────────▼──────────┐
     │  File Storage    │          │  Apache Cassandra   │
     │  (JSON/TXT)      │          │  (127.0.0.1:9042)   │
     └──────────────────┘          └─────────────────────┘
```

---

## Project Structure

```
rag-cql-lab/
│
├── README.md                    # This documentation file
│
├── rag-chatbot/                 # RAG-based Q&A chatbot
│   ├── package.json             # Node.js dependencies
│   ├── ingest.js                # Document chunking pipeline
│   ├── retrieve.js              # Keyword-based retrieval
│   ├── chat.js                  # Main chat interface
│   ├── data/
│   │   ├── docs.txt             # Source documents
│   │   └── chunks.json          # Processed chunks (generated)
│   └── .gitignore
│
└── cql-agent/                   # Natural language to CQL agent
    ├── package.json             # Node.js dependencies
    ├── schema.cql               # Cassandra schema definition
    ├── agent.js                 # LLM-powered CQL generator
    ├── db.js                    # Cassandra client setup
    ├── run.js                   # Entry point & demo queries
    └── .gitignore
```

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **Node.js** | Latest | Runtime environment (ES Modules) |
| **Google Generative AI** | ^0.24.1 | Gemini 2.0 Flash LLM integration |
| **Apache Cassandra** | 4.x | Distributed NoSQL database |
| **Cassandra Driver** | ^4.8.0 | Node.js Cassandra client |

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

3. **Apache Cassandra** (for CQL Agent module only)
   - Running locally on `127.0.0.1:9042`
   - Or use Docker:
     ```bash
     docker run -d --name cassandra -p 9042:9042 cassandra:latest
     ```

4. **Google Gemini API Key**
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
# For RAG Chatbot
cd rag-chatbot
npm install

# For CQL Agent
cd ../cql-agent
npm install
```

---

## Module 1: RAG Chatbot

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

## Module 2: CQL Agent

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

**4. "Module not found" errors**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
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
