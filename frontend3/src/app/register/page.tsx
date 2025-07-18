"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import RegisterForm from "@/app/components/registro_form"; // Assumindo que este componente será adaptado também

// Define os tipos de usuário para controle do estado
type UserType = 'gerente' | 'funcionario';

export default function RegisterPage() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>('gerente');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-teal-500 p-6">
      <main className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-2">
          Crie sua Conta
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Comece a gerenciar suas tarefas e equipes.
        </p>

        {/* Seletor de tipo de conta */}
        <div className="flex justify-center border-b-2 border-gray-200 mb-6">
          <button
            onClick={() => setUserType('gerente')}
            className={`px-6 py-2 text-sm font-semibold transition-colors duration-300 focus:outline-none ${
              userType === 'gerente'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-blue-600'
            }`}
          >
            Sou Gerente
          </button>
          <button
            onClick={() => setUserType('funcionario')}
            className={`px-6 py-2 text-sm font-semibold transition-colors duration-300 focus:outline-none ${
              userType === 'funcionario'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-500 hover:text-blue-600'
            }`}
          >
            Sou Funcionário
          </button>
        </div>

        {/* O tipo de usuário é passado para o formulário */}
        <RegisterForm userType={userType} />

        <p className="text-center text-sm text-gray-600 mt-6">
          Já tem uma conta?{" "}
          <button
            onClick={() => router.push("/login")}
            className="text-blue-600 font-medium hover:underline"
          >
            Entrar
          </button>
        </p>
      </main>
    </div>
  );
}
