import { useState, useEffect } from "react";
import type { Habito } from "@/app/types/habit";

const lista_habitos_route = "http://localhost:8000/habitos";

export function useHabits() {
  const [habits, setHabits] = useState<Habito[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHabits = async () => {
      setLoading(true);
      try {
        const response = await fetch(lista_habitos_route);
        if (!response.ok) {
          throw new Error("Falha ao carregar hábitos");
        }
        const data: Habito[] = await response.json();
        setHabits(data);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("Erro inesperado");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchHabits();
  }, []);

  return { habits, loading, error };
}
