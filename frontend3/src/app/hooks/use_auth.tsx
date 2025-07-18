"use client";
import { useState, useEffect } from 'react';

interface AuthUser {
  id: number | null;
  nome: string | null;
  tipo: 'instrutor' | 'aluno' | null;
}

export const useAuth = (): AuthUser => {
  const [user, setUser] = useState<AuthUser>({ id: null, nome: null, tipo: null });

  useEffect(() => {
    if (typeof window !== "undefined") {
      const id = localStorage.getItem("user_id");
      const nome = localStorage.getItem("user_name");
      const tipo = localStorage.getItem("user_type") as 'instrutor' | 'aluno' | null;
      setUser({
        id: id ? parseInt(id, 10) : null,
        nome,
        tipo,
      });
    }
  }, []);

  return user;
};