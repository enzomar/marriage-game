import Database from "better-sqlite3";
import path from "path";

const db = new Database(path.resolve("./db.sqlite"));
db.prepare(`CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT
)`).run();

export async function GET() {
  const rows = db.prepare("SELECT * FROM questions ORDER BY id DESC").all();
  return new Response(JSON.stringify(rows), { status: 200 });
}
