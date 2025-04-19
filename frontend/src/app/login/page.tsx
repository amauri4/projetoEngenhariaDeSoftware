"use client";

import { useRouter } from "next/navigation";
import LoginForm from "@/app/components/login_form";

export default function LoginPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-6">
      <main className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-indigo-700 mb-2">
          Bem-vindo de volta!
        </h1>
        <p className="text-center text-gray-600 mb-6">
          Faça login na sua conta HabitTracker
        </p>

        <LoginForm />

        <p className="text-center text-sm text-gray-600 mt-6">
          Ainda não tem uma conta?{" "}
          <button
            onClick={() => router.push("/register")}
            className="text-indigo-600 font-medium hover:underline"
          >
            Criar conta
          </button>
        </p>
      </main>
    </div>
  );
}
