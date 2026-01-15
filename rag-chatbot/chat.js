import { retrieveRelevantChunks } from "./retrieve.js";
import { GoogleGenerativeAI } from "@google/generative-ai";

console.log("Initializing Gemini client...");

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const llm = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

async function runRagChatbot(question) {
  console.log("\nUser question:", question);

  const retrievedContext = retrieveRelevantChunks(question);

  if (!retrievedContext.length) {
    console.log("No relevant data found.");
    return;
  }

  const finalPrompt = `
You are a RAG-based assistant.
Answer strictly from the provided context.

Context:
${retrievedContext.join("\n")}

Question:
${question}
`;

  console.log("\nSending prompt to Gemini...");
  const response = await llm.generateContent(finalPrompt);

  console.log("\nGemini response:\n");
  console.log(response.response.text());
}

/* ---------- TEST QUERIES ---------- */

await runRagChatbot("What is Cassandra?");
await runRagChatbot("Explain RAG");
await runRagChatbot("What is CQL?");
