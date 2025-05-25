import { useCallback, useState } from "react";
import {
  listarDiasHabitoSemana,
  adicionarDiaHabitoSemana,
  adicionarVariosDiasSemana,
  removerDiaPorId,
  removerDiaPorHabitoEDia,
  removerTodosDiasHabitoSemana,
} from "@/app/services/dia_habito_semana_service";

export function useDiaHabitoSemana() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const listarDias = useCallback(async (habito_id: number) => {
    setLoading(true);
    setError(null);
    try {
      return await listarDiasHabitoSemana(habito_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const adicionarDia = useCallback(
    async (habito_id: number, dia: number) => {
      setLoading(true);
      setError(null);
      try {
        return await adicionarDiaHabitoSemana(habito_id, dia);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const adicionarVariosDias = useCallback(
    async (habito_id: number, dias: number[]) => {
      setLoading(true);
      setError(null);
      try {
        return await adicionarVariosDiasSemana(habito_id, dias);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const removerDia = useCallback(
    async (dia: number) => {
      setLoading(true);
      setError(null);
      try {
        return await removerDiaPorId(dia);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const removerPorHabitoDia = useCallback(
    async (habito_id: number, dia: number) => {
      setLoading(true);
      setError(null);
      try {
        return await removerDiaPorHabitoEDia(habito_id,dia);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const removerTodosDias = useCallback(
    async (habito_id: number) => {
      setLoading(true);
      setError(null);
      try {
        return await removerTodosDiasHabitoSemana(habito_id);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    listarDias,
    adicionarDia,
    adicionarVariosDias,
    removerDia,
    removerPorHabitoDia,
    removerTodosDias,
    loading,
    error,
  };
}