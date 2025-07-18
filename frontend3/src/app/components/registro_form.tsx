"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { registerInstrutorService, registerAlunoService } from "@/app/services/registro_usuarios_service";

type UserType = 'instrutor' | 'aluno';

interface FormData {
    nome: string;
    email: string;
    senha: string;
    instrutor_id?: string; 
}

interface RegisterFormProps {
  userType: UserType;
}

export default function RegisterForm({ userType }: RegisterFormProps) {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const [formData, setFormData] = useState<FormData>({
        nome: "",
        email: "",
        senha: "",
        instrutor_id: "",
    });

    useEffect(() => {
        setFormData({
            nome: "",
            email: "",
            senha: "",
            instrutor_id: "",
        });
        setError(null); 
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
        setLoading(true);
        setError(null);
        
        const payload: any = {
            nome: formData.nome,
            email: formData.email,
            senha: formData.senha,
        };

        if (userType === 'aluno' && formData.instrutor_id) {
            payload.instrutor_id = parseInt(formData.instrutor_id, 10);
        }

        try {
            if (userType === 'instrutor') {
                await registerInstrutorService(payload);
            } else {
                await registerAlunoService(payload);
            }
            router.push("/login?message=Conta criada com sucesso!");

        } catch (err) {
            setError(err instanceof Error ? err.message : "Ocorreu um erro desconhecido.");
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

            {userType === 'aluno' && (
                <InputField
                    id="instrutor_id"
                    label="ID do Instrutor (Opcional)"
                    type="number"
                    value={formData.instrutor_id || ''}
                    onChange={handleChange}
                    placeholder="ID do seu instrutor"
                    required={false} 
                    disabled={loading}
                />
            )}

            {error && (
                <div
                    className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
                    role="alert"
                >
                    {error}
                </div>
            )}

            <button
                type="submit"
                disabled={loading}
                className="w-full bg-orange-600 hover:bg-orange-700 text-white font-semibold py-2 rounded-lg transition duration-300 disabled:opacity-50"
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
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:outline-none disabled:bg-gray-100"
                placeholder={placeholder}
            />
        </div>
    );
}