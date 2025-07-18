"use client";
import { useState, useEffect } from 'react';

interface AuthUser {
  id: number | null;
  nome: string | null;
  tipo: 'gerente' | 'funcionario' | null;
}

export const useAuth = (): AuthUser => {
  const [user, setUser] = useState<AuthUser>({ id: null, nome: null, tipo: null });

  useEffect(() => {
    if (typeof window !== "undefined") {
      const id = localStorage.getItem("user_id");
      const nome = localStorage.getItem("user_name");
      const tipo = localStorage.getItem("user_type") as 'gerente' | 'funcionario' | null;
      setUser({
        id: id ? parseInt(id, 10) : null,
        nome,
        tipo,
      });
    }
  }, []);

  return user;
};