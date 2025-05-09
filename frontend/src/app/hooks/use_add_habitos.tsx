"use client";

import { useState } from "react";
import { addHabitService } from "@/app/services/add_habit_service";
import { HabitoUsuarioSchema, type HabitoCreateInput } from "@/app/schemas/HabitoUsuarioSchema";
import { HabitoUsuario } from "@/app/types/habito_usuario";
import { z } from 'zod';
import { Frequencia } from "@/app/types/frequencia";

const useAddHabit = (usuarioId: number) => {
  const [loadingHabit, setLoading] = useState(false);
  const [errorHabit, setError] = useState<string | null>(null);

  const addHabit = async (
    habitoBaseId: number,
    descricao: string,
    frequencia: Frequencia,
    dataInicio: string,
    vezesNaSemana?: number | null,
    diasSemana?: number[],
    diasMes?: number[]
  ): Promise<HabitoUsuario | null> => {
    setLoading(true);
    setError(null);

    try {
      // Validação dos dados
      const validatedData: HabitoCreateInput = HabitoUsuarioSchema.parse({
        habitoBaseId,
        descricao,
        frequencia,
        dataInicio,
        vezesNaSemana: frequencia === Frequencia.SEMANAL ? vezesNaSemana : null,
        diasSemana: frequencia === Frequencia.DIARIA ? diasSemana : undefined,
        diasMes: frequencia === Frequencia.MENSAL ? diasMes : undefined,
        usuarioId
      });

      // Chamada ao serviço
      return await addHabitService({
        ...validatedData,
        // Garante que arrays vazios não sejam enviados
        diasSemana: validatedData.diasSemana || undefined,
        diasMes: validatedData.diasMes || undefined
      });
    } catch (err) {
      // Tratamento de erros
      if (err instanceof z.ZodError) {
        const errorMessages = err.errors
          .map(e => {
            // Mensagens mais amigáveis para o usuário
            if (e.path.includes('diasSemana')) return "Selecione os dias da semana";
            if (e.path.includes('diasMes')) return "Selecione os dias do mês";
            return e.message;
          })
          .filter((msg, i, arr) => arr.indexOf(msg) === i) // Remove duplicados
          .join(". ");
        
        setError(`Erro no formulário: ${errorMessages}`);
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Ocorreu um erro desconhecido ao adicionar o hábito");
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