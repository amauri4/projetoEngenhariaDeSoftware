"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const login_route = "http://localhost:8000/usuarios/login";

export default function LoginForm() {
  const router = useRouter();
  const [formData, setFormData] = useState({ email: "", senha: "" });
  const [erroMensagem, setErroMensagem] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.id]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErroMensagem("");

    try {
      const response = await fetch(login_route, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("auth_token", data.access_token);
        localStorage.setItem("usuario_id", data.usuario.id);
        localStorage.setItem("email", data.usuario.email);
        router.push("/dashboard"); 
      } else {
        const error = await response.json();
        setErroMensagem("Erro: " + (error.erro || "Credenciais inválidas"));
      }
    } catch (error) {
      console.error("Erro ao fazer login:", error);
      setErroMensagem("Erro na conexão com o servidor.");
    }
  };

  return (
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
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
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
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
          placeholder="••••••••"
        />
      </div>

      {erroMensagem && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <span className="block sm:inline">{erroMensagem}</span>
        </div>
      )}

      <button
        type="submit"
        className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg transition duration-300"
      >
        Entrar
      </button>
    </form>
  );
}
