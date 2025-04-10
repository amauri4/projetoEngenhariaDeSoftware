"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 text-white p-6">
      <main
        className="max-w-xl rounded-2xl p-10 text-center shadow-xl backdrop-blur-md"
        style={{
          backgroundColor: "var(--card-background)",
        }}
      >
        <h1 className="text-4xl font-bold mb-4">Bem-vindo ao HabitTracker!</h1>
        <p className="text-lg mb-6">
          Gerencie seus hábitos de forma simples e eficaz. Crie metas diárias, acompanhe seu progresso e mantenha o foco no que realmente importa.
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => router.push("/login")}
            className="bg-white text-indigo-600 font-semibold py-2 px-6 rounded-xl hover:bg-indigo-100 transition duration-300"
          >
            Entrar
          </button>
          <button
            onClick={() => router.push("/register")}
            className="bg-indigo-700 hover:bg-indigo-800 text-white font-semibold py-2 px-6 rounded-xl transition duration-300"
          >
            Criar Conta
          </button>
        </div>
      </main>
    </div>
  );
}
