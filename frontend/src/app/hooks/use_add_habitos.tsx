"use client";

import { useState } from "react";
import { addHabitService } from "@/app/services/add_habit_service";
import { HabitoUsuarioSchema, type HabitoCreateInput } from "@/app/schemas/HabitoUsuarioSchema";
import { HabitoUsuario } from "@/app/types/habito_usuario";
import { z } from 'zod'
import { Frequencia } from "@/app/types/frequencia";

const useAddHabit = (usuarioId: number) => {
  const [loadingHabit, setLoading] = useState(false);
  const [errorHabit, setError] = useState<string | null>(null);

  const addHabit = async (
    habitoBaseId: number,
    descricao: string,
    frequencia: Frequencia,
    dataInicio: Date,
    vezesNaSemana?: number | null
  ): Promise<HabitoUsuario | null> => {
    setLoading(true);
    setError(null);

    try {

      const validatedData: HabitoCreateInput = HabitoUsuarioSchema.parse({
        habitoBaseId,
        descricao,
        frequencia,
        dataInicio,
        vezesNaSemana,
        usuarioId
      });

      return await addHabitService(validatedData);
    } catch (err) {

      if (err instanceof z.ZodError) {
        const errorMessages = err.errors.map(e => e.message).join(", ");
        setError(`Erro de validação: ${errorMessages}`);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Ocorreu um erro desconhecido");
      }
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { 
    addHabit, 
    loadingHabit, 
    errorHabit,
    resetError: () => setError(null) 
  };
};

export default useAddHabit;