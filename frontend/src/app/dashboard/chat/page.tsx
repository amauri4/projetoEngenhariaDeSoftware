"use client";

import { useEffect, useState } from "react";
import { HabitoUsuario } from "../../types/habito_usuario";

export default function ChatAssistentePage() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState<
    { from: "user" | "bot"; text: string }[]
  >([]);
  const [habits, setHabits] = useState<HabitoUsuario[]>([]);
  const [usuarioId, setUsuarioId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const id = localStorage.getItem("usuario_id");
    if (id) setUsuarioId(parseInt(id));
  }, []);

  useEffect(() => {
    async function fetchHabitsUsuario() {
      if (!usuarioId) return;
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/habitos/usuario/${usuarioId}`
      );
      const data = await res.json();
      setHabits(data);
    }

    if (usuarioId) fetchHabitsUsuario();
  }, [usuarioId]);

  async function sendMessage() {
    if (!message.trim()) return;

    setChatLog((prev) => [...prev, { from: "user", text: message }]);
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/llm/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: "Usuário", 
          message,
          habits,
        }),
      });

      if (!res.ok) throw new Error("Erro na resposta do servidor");

      const data = await res.json();
      setChatLog((prev) => [...prev, { from: "bot", text: data.response }]);
    } catch (error) {
      setChatLog((prev) => [
        ...prev,
        { from: "bot", text: "Erro ao conversar com o assistente." },
      ]);
    } finally {
      setLoading(false);
      setMessage("");
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold mb-4 text-indigo-600">IAbit</h1>

        <div className="h-96 overflow-y-auto border rounded p-4 mb-4 bg-gray-50">
          {chatLog.map((msg, i) => (
            <div
              key={i}
              className={`mb-2 ${
                msg.from === "user" ? "text-right" : "text-left text-blue-700"
              }`}
            >
              <div className="inline-block bg-gray-200 rounded px-3 py-2">
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={3}
          placeholder="Digite sua pergunta..."
          className="w-full border rounded p-2 mb-2"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition disabled:opacity-50"
        >
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </div>
  );
}