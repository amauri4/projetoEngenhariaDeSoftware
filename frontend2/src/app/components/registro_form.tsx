"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

type UserType = 'gerente' | 'funcionario';

interface FormData {
    nome: string;
    email: string;
    senha: string;
    chefe_id?: string; 
}

interface RegisterFormProps {
  userType: UserType;
}

export default function RegisterForm({ userType }: RegisterFormProps) {
    const router = useRouter();
    const [formData, setFormData] = useState<FormData>({
        nome: "",
        email: "",
        senha: "",
        chefe_id: "",
    });
    const [erroMensagem, setErroMensagem] = useState<string>("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setFormData({
            nome: "",
            email: "",
            senha: "",
            chefe_id: "",
        });
        setErroMensagem("");
    }, [userType]);

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
        setLoading(true);

        const isGerente = userType === 'gerente';
        const endpoint = isGerente ? "/auth/gerentes/registrar" : "/auth/funcionarios/registrar";
        
        const payload: any = {
            nome: formData.nome,
            email: formData.email,
            senha: formData.senha,
        };

        if (!isGerente && formData.chefe_id) {
            payload.chefe_id = parseInt(formData.chefe_id, 10);
        }

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const { erro } = await response.json();
                throw new Error(erro || "Não foi possível registrar.");
            }

            router.push("/login?message=Conta criada com sucesso!");
        } catch (error) {
            console.error("Erro ao registrar:", error);
            setErroMensagem(error instanceof Error ? error.message : "Erro desconhecido.");
        } finally {
            setLoading(false);
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
                disabled={loading}
            />

            <InputField
                id="email"
                label="E-mail"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="seuemail@exemplo.com"
                disabled={loading}
            />

            <InputField
                id="senha"
                label="Senha"
                type="password"
                value={formData.senha}
                onChange={handleChange}
                placeholder="••••••••"
                disabled={loading}
            />

            {/* Campo condicional para ID do Chefe */}
            {userType === 'funcionario' && (
                <InputField
                    id="chefe_id"
                    label="ID do Chefe (Opcional)"
                    type="number"
                    value={formData.chefe_id || ''}
                    onChange={handleChange}
                    placeholder="ID do seu gerente"
                    required={false} 
                    disabled={loading}
                />
            )}

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
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50"
            >
                {loading ? "Criando conta..." : "Criar Conta"}
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
    required?: boolean;
    disabled?: boolean;
}

function InputField({ id, label, type, value, onChange, placeholder, required = true, disabled = false }: InputFieldProps) {
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
                required={required}
                disabled={disabled}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:bg-gray-100"
                placeholder={placeholder}
            />
        </div>
    );
}
