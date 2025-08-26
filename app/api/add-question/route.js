import Database from "better-sqlite3";
import path from "path";

const db = new Database(path.resolve("./db.sqlite"));
db.prepare(`CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT
)`).run();

export async function POST(req) {
  const body = await req.json();
  const { question } = body;
  if (!question) return new Response(JSON.stringify({ error: "Question required" }), { status: 400 });

  const stmt = db.prepare("INSERT INTO questions (text) VALUES (?)");
  const info = stmt.run(question);

  return new Response(JSON.stringify({ id: info.lastInsertRowid, text: question }), { status: 200 });
}
