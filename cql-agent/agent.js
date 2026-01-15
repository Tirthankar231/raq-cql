import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const llm = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

export async function generateCqlQuery(schemaContext, userQuestion) {
  console.log("\nConverting question to CQL...");

  const prompt = `
You are an expert Cassandra engineer.

Schema:
${schemaContext}

Convert the user request into a valid Cassandra CQL query.
Important: If filtering on non-primary key columns, add ALLOW FILTERING at the end of the query.
Return only the query, nothing else.

User request: ${userQuestion}
`;

  const response = await llm.generateContent(prompt);
  let query = response.response.text();
  // Remove markdown code blocks and language identifiers
  query = query.replace(/```(?:sql|cql)?\n?/gi, "").trim();
  // Remove standalone "cql" or "sql" lines at the start
  query = query.replace(/^(cql|sql)\s*/i, "").trim();
  return query;
}
