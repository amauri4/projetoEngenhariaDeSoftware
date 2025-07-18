"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-yellow-400 to-orange-500 text-white p-6">
      <main
        className="max-w-xl rounded-2xl p-10 text-center shadow-xl backdrop-blur-md"
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.1)", 
        }}
      >
        <h1 className="text-4xl font-bold mb-4">Gerenciador de Treinos</h1>
        <p className="text-lg mb-6">
          Crie e acompanhe seus treinos personalizados. Atribua exercícios, monitore o progresso e alcance seus objetivos.
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => router.push("/login")}
            className="bg-white text-orange-600 font-semibold py-2 px-6 rounded-xl hover:bg-orange-100 transition duration-300"
          >
            Entrar
          </button>
          <button
            onClick={() => router.push("/register")}
            className="bg-orange-600 hover:bg-orange-700 text-white font-semibold py-2 px-6 rounded-xl transition duration-300"
          >
            Criar Conta
          </button>
        </div>
      </main>
    </div>
  );
}