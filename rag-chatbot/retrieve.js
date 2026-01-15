import fs from "fs";

const storedChunks = JSON.parse(
  fs.readFileSync("./data/chunks.json", "utf-8")
);

export function retrieveRelevantChunks(userQuery) {
  console.log("Searching documents for:", userQuery);

  // Extract keywords from query (remove common words)
  const stopWords = ["what", "is", "the", "a", "an", "how", "why", "explain", "tell", "me", "about"];
  const keywords = userQuery
    .toLowerCase()
    .replace(/[^\w\s]/g, '')  // Remove punctuation
    .split(/\s+/)
    .filter(word => word.length > 2 && !stopWords.includes(word));

  // Find chunks that contain any of the keywords
  const matches = storedChunks.filter(chunk => {
    const chunkLower = chunk.toLowerCase();
    return keywords.some(keyword => chunkLower.includes(keyword));
  });

  console.log("Relevant chunks found:", matches.length);
  return matches;
}
