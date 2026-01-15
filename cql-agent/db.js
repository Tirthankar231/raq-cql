import cassandra from "cassandra-driver";

console.log("Initializing Cassandra client...");

export const cassandraClient = new cassandra.Client({
  contactPoints: ["127.0.0.1"],
  localDataCenter: "datacenter1",
  keyspace: "agent_demo"
});
