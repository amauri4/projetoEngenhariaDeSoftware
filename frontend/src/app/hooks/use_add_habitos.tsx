"use client";

import { useState } from "react";
import { addHabitService } from "@/app/services/add_habit_service";
import { HabitoUsuario } from "@/app/types/habito_usuario";

const useAddHabit = (usuarioId: number | null) => {
  const [loadingHabit, setLoading] = useState(false);
  const [errorHabit, setError] = useState<string | null>(null);

  const addHabit = async (habitoBaseId: number | null, descricao: string | null): Promise<HabitoUsuario | null> => {
    if (!usuarioId || !habitoBaseId || !descricao) {
      setError("Dados inválidos");
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      return await addHabitService(usuarioId, habitoBaseId, descricao);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { addHabit, loadingHabit, errorHabit };
};

export default useAddHabit;
