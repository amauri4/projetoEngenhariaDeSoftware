"use client";

import { useEffect, useState } from "react";
import { fetchHabitosUsuario } from "@/app/services/habit_service";
import type { HabitoUsuario } from "@/app/types/habito_usuario";

export function useHabitosUsuario(usuarioId: number | null, refreshKey: number = 0) {
  const [habitsUsuario, setHabitsUsuario] = useState<HabitoUsuario[]>([]);
  const [loadingUsuario, setLoading] = useState<boolean>(false);
  const [errorUsuario, setError] = useState<string | null>(null);

  useEffect(() => {
    if (usuarioId === null) {
      setHabitsUsuario([]);
      setLoading(false);
      setError(null);
      return;
    }

    const fetchHabits = async () => {
      setLoading(true);
      setError(null);

      try {
        const email = localStorage.getItem("email");
        if (!email) {
          throw new Error("Email não encontrado.");
        }

        const habitos = await fetchHabitosUsuario(email);
        setHabitsUsuario(habitos);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Erro desconhecido");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchHabits();
  }, [usuarioId, refreshKey]);

  return { habitsUsuario, loadingUsuario, errorUsuario };
}
