import fs from "fs";
import { cassandraClient } from "./db.js";
import { generateCqlQuery } from "./agent.js";

const schemaContext = fs.readFileSync("./schema.cql", "utf-8");

async function runCqlAgent(question) {
  console.log("USER QUESTION:", question);

  const generatedQuery = await generateCqlQuery(schemaContext, question);

  console.log("\nGenerated CQL:");
  console.log(generatedQuery);

  const result = await cassandraClient.execute(generatedQuery);

  console.log("\nQuery Result:");
  console.table(result.rows);
}

(async () => {
  console.log("Starting CQL Agent...");
  await cassandraClient.connect();
  console.log("Cassandra connected.");

  await runCqlAgent("Show all users");
  await runCqlAgent("Show users created on 2026-01-15");
  await runCqlAgent("List email and name of users");

  process.exit();
})();
