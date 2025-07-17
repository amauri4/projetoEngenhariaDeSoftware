"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-teal-500 text-white p-6">
      <main
        className="max-w-xl rounded-2xl p-10 text-center shadow-xl backdrop-blur-md"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.1)", 
        }}
      >
        <h1 className="text-4xl font-bold mb-4">Gerenciador de Tarefas</h1>
        <p className="text-lg mb-6">
          Organize as tarefas da sua equipe de forma clara e eficiente. Atribua responsáveis, defina prazos e acompanhe o progresso dos seus projetos em um só lugar.
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => router.push("/login")}
            className="bg-white text-blue-600 font-semibold py-2 px-6 rounded-xl hover:bg-blue-100 transition duration-300"
          >
            Entrar
          </button>
          <button
            onClick={() => router.push("/register")}
            className="bg-blue-700 hover:bg-blue-800 text-white font-semibold py-2 px-6 rounded-xl transition duration-300"
          >
            Criar Conta
          </button>
        </div>
      </main>
    </div>
  );
}
