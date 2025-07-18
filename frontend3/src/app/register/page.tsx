"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import RegisterForm from "@/app/components/registro_form";

type UserType = 'instrutor' | 'aluno';

export default function RegisterPage() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>('instrutor');

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-yellow-400 to-orange-500 p-6">
      <main className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-orange-700 mb-2">
          Crie sua Conta
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Comece a gerenciar seus treinos e alunos.
        </p>

        <div className="flex justify-center border-b-2 border-gray-200 mb-6">
          <button
            onClick={() => setUserType('instrutor')}
            className={`px-6 py-2 text-sm font-semibold transition-colors duration-300 focus:outline-none ${
              userType === 'instrutor'
                ? 'border-b-2 border-orange-600 text-orange-600'
                : 'text-gray-500 hover:text-orange-600'
            }`}
          >
            Sou Instrutor
          </button>
          <button
            onClick={() => setUserType('aluno')}
            className={`px-6 py-2 text-sm font-semibold transition-colors duration-300 focus:outline-none ${
              userType === 'aluno'
                ? 'border-b-2 border-orange-600 text-orange-600'
                : 'text-gray-500 hover:text-orange-600'
            }`}
          >
            Sou Aluno
          </button>
        </div>

        <RegisterForm userType={userType} />

        <p className="text-center text-sm text-gray-600 mt-6">
          Já tem uma conta?{" "}
          <button
            onClick={() => router.push("/login")}
            className="text-orange-600 font-medium hover:underline"
          >
            Entrar
          </button>
        </p>
      </main>
    </div>
  );
}