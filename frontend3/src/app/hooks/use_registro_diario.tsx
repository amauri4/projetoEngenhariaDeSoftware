import { useState, useCallback } from "react";
import {
  listarRegistrosUsuario,
  listarRegistrosConcluidos,
  criarRegistroDiario,
  atualizarRegistroDiario,
  removerRegistroDiario,
  listarRegistrosPorData,
  listarRegistrosPorDataEspecifica,
} from "@/app/services/registro_habit_service";
import { RegistroDiario, RegistroDiarioCreateInput, RegistroDiarioUpdateInput } from "@/app/types/registro_habito";

export function useRegistroDiario() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getRegistrosUsuario = useCallback(async (usuario_id: number) => {
    setLoading(true);
    setError(null);
    try {
      return await listarRegistrosUsuario(usuario_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getRegistrosConcluidos = useCallback(async (usuario_id: number) => {
    setLoading(true);
    setError(null);
    try {
      return await listarRegistrosConcluidos(usuario_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const createRegistro = useCallback(async (data: RegistroDiarioCreateInput) => {
    setLoading(true);
    setError(null);
    try {
      return await criarRegistroDiario(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const updateRegistro = useCallback(
    async (registro_id: number, data: RegistroDiarioUpdateInput) => {
      setLoading(true);
      setError(null);
      try {
        return await atualizarRegistroDiario(registro_id, data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const deleteRegistro = useCallback(async (registro_id: number) => {
    setLoading(true);
    setError(null);
    try {
      await removerRegistroDiario(registro_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getRegistrosPorData = useCallback(
    async (usuario_id: number, data_inicio: string, data_fim: string) => {
      setLoading(true);
      setError(null);
      try {
        return await listarRegistrosPorData(usuario_id, data_inicio, data_fim);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erro desconhecido");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const getRegistrosPorDataEspecifica = useCallback(
    async (usuario_id: number, data: string) => {
      setLoading(true);
      setError(null);
      try {
        return await listarRegistrosPorDataEspecifica(usuario_id, data);
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
    loading,
    error,
    getRegistrosUsuario,
    getRegistrosConcluidos,
    createRegistro,
    updateRegistro,
    deleteRegistro,
    getRegistrosPorData,
    getRegistrosPorDataEspecifica,
  };
}