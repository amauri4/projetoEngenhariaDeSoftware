import { useState } from "react";
import type { Habito } from "@/app/types/habit";

const useAddHabit = (usuarioId: number | null) => {
  const [loadingHabit, setLoading] = useState(false);
  const [errorHabit, setError] = useState<string | null>(null);

  const addHabit = async (
    habitoBaseId: number | null,
    descricao: string | null
  ): Promise<Habito | null> => {
    if (!usuarioId) {
      setError("ID do usuário inválido");
      return null;
    }

    if (!habitoBaseId || !descricao) {
      setError("Dados do hábito inválidos");
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/habitos-usuario/${usuarioId}/habitos`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            descricao,
            habito_base_id: habitoBaseId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Erro ao adicionar hábito");
      }

      const data = await response.json();
      return data.habito_usuario;
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
