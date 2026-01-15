import os
from dotenv import load_dotenv

load_dotenv()

import db
from agent import create_chatbot, create_cql_agent


def run_chatbot_demo():
    """Run the RAG chatbot demo."""
    print("\n" + "=" * 60)
    print("RAG CHATBOT DEMO")
    print("=" * 60)

    chatbot = create_chatbot()

    questions = [
        "What is Cassandra?",
        "Explain RAG",
        "What is CQL?",
    ]

    for question in questions:
        print(f"\n{'─' * 40}")
        print(f"Question: {question}")
        print("─" * 40)
        chatbot.print_response(question)


def run_cql_agent_demo():
    """Run the CQL agent demo."""
    print("\n" + "=" * 60)
    print("CQL AGENT DEMO")
    print("=" * 60)

    db.connect()
    cql_agent = create_cql_agent()

    queries = [
        "Show all users",
        "Show users created on 2026-01-15",
        "List email and name of users",
    ]

    try:
        for query in queries:
            print(f"\n{'─' * 40}")
            print(f"Request: {query}")
            print("─" * 40)
            cql_agent.print_response(query)
    finally:
        db.close()


def main():
    print("Starting Agno Agent Lab...")

    # Run RAG chatbot demo
    run_chatbot_demo()

    # Run CQL agent demo
    run_cql_agent_demo()

    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
