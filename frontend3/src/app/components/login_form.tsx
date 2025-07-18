"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginGerenteService, loginFuncionarioService } from "@/app/services/registro_usuarios_service";

type UserType = 'gerente' | 'funcionario';

export default function LoginForm() {
  const router = useRouter();
  const [userType, setUserType] = useState<UserType>('gerente');
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
      if (userType === 'gerente') {
        authenticatedUser = await loginGerenteService(formData);
      } else {
        authenticatedUser = await loginFuncionarioService(formData);
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
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:bg-gray-100"
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
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:bg-gray-100"
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
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </>
  );
}
