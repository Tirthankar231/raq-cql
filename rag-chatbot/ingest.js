import fs from "fs";

console.log("Starting document ingestion --->>>>");

const rawText = fs.readFileSync("./data/docs.txt", "utf-8");

const documentChunks = rawText
  .split("\n")
  .map(line => line.trim())
  .filter(Boolean);

fs.writeFileSync(
  "./data/chunks.json",
  JSON.stringify(documentChunks, null, 2)
);

console.log("Ingestion complete.");
console.log("Total chunks stored:", documentChunks.length);
