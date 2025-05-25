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

  // 🔐 Recupera o ID do usuário do localStorage
  useEffect(() => {
    const id = localStorage.getItem("usuario_id");
    if (id) setUsuarioId(parseInt(id));
  }, []);

  // 🔗 Busca os hábitos do usuário
  useEffect(() => {
    async function fetchHabitsUsuario() {
      if (!usuarioId) return;
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/habitos/usuario/${usuarioId}`
        );
        const data = await res.json();
        setHabits(data);
      } catch (error) {
        console.error("Erro ao buscar hábitos", error);
      }
    }

    if (usuarioId) fetchHabitsUsuario();
  }, [usuarioId]);

  // ✉️ Envia mensagem para o backend/chatbot
  async function sendMessage() {
    if (!message.trim()) return;

    const userMessage = { from: "user" as const, text: message };
    setChatLog((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: usuarioId,
          mensagem: message,
        }),
      });

      if (!res.ok) throw new Error("Erro na resposta do servidor");

      const data = await res.json();

      const botMessage = { from: "bot" as const, text: data.resposta };
      setChatLog((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      setChatLog((prev) => [
        ...prev,
        {
          from: "bot",
          text: "❌ Ocorreu um erro ao conversar com o assistente.",
        },
      ]);
    } finally {
      setLoading(false);
      setMessage("");
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-md p-6">
        <h1 className="text-3xl font-bold mb-6 text-indigo-600 text-center">
           IAbit - Seu Assistente de Hábitos
        </h1>

        <div className="h-[400px] overflow-y-auto border rounded-xl p-4 mb-4 bg-gray-50">
          {chatLog.map((msg, i) => (
            <div
              key={i}
              className={`mb-2 ${
                msg.from === "user" ? "text-right" : "text-left"
              }`}
            >
              <div
                className={`inline-block px-4 py-2 rounded-xl ${
                  msg.from === "user"
                    ? "bg-indigo-500 text-white"
                    : "bg-gray-200 text-gray-900"
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="text-left">
              <div className="inline-block px-4 py-2 rounded-xl bg-gray-200">
                Digitando...
              </div>
            </div>
          )}
        </div>

        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={3}
          placeholder="Digite sua mensagem e aperte Enter..."
          className="w-full border rounded-xl px-4 py-2 mb-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="w-full bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition disabled:opacity-50"
        >
          {loading ? "Enviando..." : "Enviar"}
        </button>
      </div>
    </div>
  );
}
