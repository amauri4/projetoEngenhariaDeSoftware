"use client";

import { useState } from "react";
import { deleteHabitoUsuario } from "@/app/services/delete_habit_service";

const useDeleteHabit = () => {
  const [loadingDeleteHabit, setLoading] = useState(false);
  const [errorDeleteHabit, setError] = useState<string | null>(null);

  const deleteHabit = async (habitoUsuarioId: number | null): Promise<boolean> => {
    if (!habitoUsuarioId) {
      setError("ID do hábito inválido");
      return false;
    }

    setLoading(true);
    setError(null);

    try {
      await deleteHabitoUsuario(habitoUsuarioId);
      return true;
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Erro desconhecido");
      }
      return false;
    } finally {
      setLoading(false);
    }
  };

  return { deleteHabit, loadingDeleteHabit, errorDeleteHabit };
};

export default useDeleteHabit;
