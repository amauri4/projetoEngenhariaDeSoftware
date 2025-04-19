"use client";

import { useRouter } from "next/navigation";
import RegisterForm from "@/app/components/registro_form";

export default function RegisterPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-6">
      <main className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-indigo-700 mb-2">
          Criar Conta
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Comece sua jornada no HabitTracker
        </p>

        <RegisterForm />

        <p className="text-center text-sm text-gray-600 mt-6">
          Já tem uma conta?{" "}
          <button
            onClick={() => router.push("/login")}
            className="text-indigo-600 font-medium hover:underline"
          >
            Entrar
          </button>
        </p>
      </main>
    </div>
  );
}
