"use client";

import { useState, useEffect } from "react";
import { fetchHabitosBase } from "@/app/services/habito_base_service";
import type { HabitoBase } from "@/app/types/habito_base";

export function useHabits() {
  const [habits, setHabits] = useState<HabitoBase[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await fetchHabitosBase();
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

    fetchData();
  }, []);

  return { habits, loading, error };
}
