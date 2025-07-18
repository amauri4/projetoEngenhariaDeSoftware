"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginInstrutorService, loginAlunoService } from "@/app/services/registro_usuarios_service";

type UserType = 'instrutor' | 'aluno';

export default function LoginForm() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>('instrutor');
  const [formData, setFormData] = useState({ email: "", senha: "" });
  const [erroMensagem, setErroMensagem] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.id]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErroMensagem("");
    setLoading(true);

    try {
      let authenticatedUser;
      if (userType === 'instrutor') {
        authenticatedUser = await loginInstrutorService(formData);
      } else {
        authenticatedUser = await loginAlunoService(formData);
      }

      if (typeof window !== "undefined") {
        localStorage.setItem("user_id", authenticatedUser.id.toString());
        localStorage.setItem("user_type", authenticatedUser.tipo_ator);
        localStorage.setItem("user_name", authenticatedUser.nome);
      }
      
      router.push("/dashboard");

    } catch (error: any) {
      console.error("Erro ao fazer login:", error);
      setErroMensagem(error.message || "Erro na conexão com o servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
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

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            E-mail
          </label>
          <input
            id="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={loading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none disabled:bg-gray-100"
            placeholder="seuemail@exemplo.com"
          />
        </div>

        <div>
          <label htmlFor="senha" className="block text-sm font-medium text-gray-700 mb-1">
            Senha
          </label>
          <input
            id="senha"
            type="password"
            value={formData.senha}
            onChange={handleChange}
            required
            disabled={loading}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none disabled:bg-gray-100"
            placeholder="••••••••"
          />
        </div>

        {erroMensagem && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span className="block sm:inline">{erroMensagem}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-orange-600 hover:bg-orange-500 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </>
  );
}