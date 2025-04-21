import { useEffect, useState } from "react";
import type { Habito } from "@/app/types/habit";

export function useHabitosUsuario(usuarioId: number | null) {
  const [habitsUsuario, setHabitsUsuario] = useState<Habito[]>([]);
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

        const response = await fetch(`http://localhost:8000/habitos-usuario/${email}/habitos`);

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.erro || "Erro ao buscar hábitos do usuário.");
        }

        const data: Habito[] = await response.json();
        setHabitsUsuario(data);
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
  }, [usuarioId]);

  return { habitsUsuario, loadingUsuario, errorUsuario };
}
