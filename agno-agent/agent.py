from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.toolkit import Toolkit

from db import execute_query
from knowledge import load_documents, retrieve_relevant_chunks

# Load knowledge base on module import
KNOWLEDGE_CHUNKS = load_documents()

CASSANDRA_SCHEMA = """
CREATE TABLE agent_demo.users (
  id UUID PRIMARY KEY,
  name TEXT,
  email TEXT,
  created_at DATE
);
"""


class RAGTools(Toolkit):
    """Tools for RAG-based question answering."""

    def __init__(self):
        super().__init__(name="rag_tools")
        self.register(self.search_knowledge_base)

    def search_knowledge_base(self, query: str) -> str:
        """
        Search the knowledge base for information relevant to the query.

        Args:
            query: The search query to find relevant information.

        Returns:
            Relevant context from the knowledge base.
        """
        matches = retrieve_relevant_chunks(query, KNOWLEDGE_CHUNKS)
        if not matches:
            return "No relevant information found in the knowledge base."
        return "\n".join(matches)


class CQLTools(Toolkit):
    """Tools for executing CQL queries against Cassandra."""

    def __init__(self):
        super().__init__(name="cql_tools")
        self.register(self.run_cql_query)

    def run_cql_query(self, query: str) -> str:
        """
        Execute a CQL query against the Cassandra database.

        Args:
            query: A valid CQL query string to execute.

        Returns:
            The query results as a formatted string.
        """
        try:
            results = execute_query(query)
            if not results:
                return "Query executed successfully. No rows returned."
            return str(results)
        except Exception as e:
            return f"Error executing query: {e}"


def create_chatbot() -> Agent:
    """Create the RAG chatbot agent."""
    return Agent(
        name="RAG Chatbot",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[RAGTools()],
        instructions=[
            "You are a helpful assistant that answers questions using the knowledge base.",
            "Always use the search_knowledge_base tool to find relevant information before answering.",
            "Answer strictly based on the retrieved context. If no relevant information is found, say so.",
        ],
        markdown=True,
        debug_mode=False,
    )


def create_cql_agent() -> Agent:
    """Create the CQL query generator agent."""
    return Agent(
        name="CQL Agent",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[CQLTools()],
        instructions=[
            "You are an expert Cassandra engineer.",
            f"Database Schema:\n{CASSANDRA_SCHEMA}",
            "Convert user requests into valid Cassandra CQL queries.",
            "If filtering on non-primary key columns, add ALLOW FILTERING at the end of the query.",
            "IMPORTANT: You MUST always call the run_cql_query tool to execute EVERY query. Never just display the query without executing it.",
            "After executing the query, present the results in a clear, readable format.",
        ],
        markdown=True,
        debug_mode=False,
    )
