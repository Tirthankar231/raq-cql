from cassandra.cluster import Cluster

cluster = None
session = None


def connect():
    """Connect to Cassandra database."""
    global cluster, session
    print("Connecting to Cassandra...")
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect("agent_demo")
    print("Cassandra connected.")


def execute_query(query: str) -> list[dict]:
    """Execute a CQL query and return results as a list of dictionaries."""
    if session is None:
        raise RuntimeError("Database not connected. Call connect() first.")
    result = session.execute(query)
    return [dict(row._asdict()) for row in result]


def close():
    """Close the Cassandra connection."""
    global cluster
    if cluster:
        cluster.shutdown()
        print("Cassandra connection closed.")
