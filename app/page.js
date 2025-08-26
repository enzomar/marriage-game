"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [questions, setQuestions] = useState([]);

  async function loadQuestions() {
    try {
      const res = await fetch("/api/questions");
      const data = await res.json();
      setQuestions(data);
    } catch (err) {
      console.error("Error loading questions:", err);
    }
  }

  async function submitQuestion(e) {
    e.preventDefault();
    if (!question.trim()) return;

    try {
      const res = await fetch("/api/add-question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) throw new Error("Failed to submit");
      const newQuestion = await res.json();
      setQuestions([newQuestion, ...questions]);
      setQuestion("");
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    loadQuestions();
  }, []);

  return (
    <main style={styles.container}>
      <h1 style={styles.title}>💍 Marriage Game Questions</h1>

      <form onSubmit={submitQuestion} style={styles.form}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a fun question for the bride..."
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          Submit
        </button>
      </form>

      <h2 style={styles.subtitle}>All Submitted Questions</h2>
      <div style={styles.questionsContainer}>
        {questions.length === 0 && (
          <p style={{ textAlign: "center", color: "#777" }}>No questions yet 😅</p>
        )}
        {questions.map((q) => (
          <div key={q.id} style={styles.questionCard}>
            {q.text}
          </div>
        ))}
      </div>
    </main>
  );
}

const styles = {
  container: { fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", maxWidth: "600px", margin: "40px auto", padding: "0 20px" },
  title: { textAlign: "center", color: "#ff6b81", marginBottom: "30px", fontSize: "2.2rem" },
  form: { display: "flex", gap: "10px", marginBottom: "30px" },
  input: { flex: 1, padding: "12px 16px", borderRadius: "25px", border: "2px solid #ff6b81", outline: "none", fontSize: "1rem", transition: "0.2s" },
  button: { padding: "12px 20px", backgroundColor: "#ff6b81", color: "#fff", border: "none", borderRadius: "25px", cursor: "pointer", fontWeight: "bold", fontSize: "1rem", transition: "0.2s" },
  subtitle: { color: "#555", marginBottom: "15px", fontSize: "1.5rem" },
  questionsContainer: { display: "flex", flexDirection: "column", gap: "15px" },
  questionCard: { background: "linear-gradient(135deg, #fff0f5, #ffe4e1)", padding: "15px 20px", borderRadius: "20px", boxShadow: "0 4px 8px rgba(0,0,0,0.1)", fontSize: "1.1rem", color: "#333" }
};
