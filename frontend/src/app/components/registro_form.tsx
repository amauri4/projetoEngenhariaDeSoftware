"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const REGISTRO_ROUTE = "/usuarios/registrar";

interface FormData {
    nome: string;
    email: string;
    senha: string;
}

export default function RegisterForm() {
    const router = useRouter();
    const [formData, setFormData] = useState<FormData>({
        nome: "",
        email: "",
        senha: "",
    });
    const [erroMensagem, setErroMensagem] = useState<string>("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [id]: value,
        }));
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setErroMensagem("");

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${REGISTRO_ROUTE}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                const { erro } = await response.json();
                throw new Error(erro || "Não foi possível registrar.");
            }

            router.push("/login?message=Conta criada com sucesso");
        } catch (error) {
            console.error("Erro ao registrar:", error);
            setErroMensagem(error instanceof Error ? error.message : "Erro desconhecido.");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <InputField
                id="nome"
                label="Nome completo"
                type="text"
                value={formData.nome}
                onChange={handleChange}
                placeholder="Seu nome"
            />

            <InputField
                id="email"
                label="E-mail"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="seuemail@exemplo.com"
            />

            <InputField
                id="senha"
                label="Senha"
                type="password"
                value={formData.senha}
                onChange={handleChange}
                placeholder="••••••••"
            />

            {erroMensagem && (
                <div
                    className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
                    role="alert"
                >
                    {erroMensagem}
                </div>
            )}

            <button
                type="submit"
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg transition duration-300"
            >
                Criar Conta
            </button>
        </form>
    );
}

interface InputFieldProps {
    id: keyof FormData;
    label: string;
    type: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
}

function InputField({ id, label, type, value, onChange, placeholder }: InputFieldProps) {
    return (
        <div>
            <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
                {label}
            </label>
            <input
                id={id}
                type={type}
                value={value}
                onChange={onChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                placeholder={placeholder}
            />
        </div>
    );
}
