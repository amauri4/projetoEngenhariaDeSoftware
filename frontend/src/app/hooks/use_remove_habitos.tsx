"use client";

import { useState } from "react";

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
      const response = await fetch(`http://localhost:8000/habitos-usuario/habitos/${habitoUsuarioId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.erro || "Erro ao remover hábito");
      }

      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      return false;
    } finally {
      setLoading(false);
    }
  };

  return { deleteHabit, loadingDeleteHabit, errorDeleteHabit };
};

export default useDeleteHabit;
