"use client";

import { useState, useEffect, useCallback } from "react";
import { Tarefa } from "@/app/types/tarefa";
import { getTarefasByAtorService, deleteTarefaService } from "@/app/services/tarefa_service";

/**
 * Hook customizado para gerenciar o estado das tarefas (listar, remover, etc.).
 * @param atorId - O ID do ator (gerente ou funcionário) para buscar as tarefas.
 */
export const useTarefas = (atorId: number | null) => {
  const [tarefas, setTarefas] = useState<Tarefa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar as tarefas, memorizada com useCallback
  const fetchTarefas = useCallback(async () => {
    if (!atorId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await getTarefasByAtorService(atorId);
      setTarefas(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar tarefas.");
    } finally {
      setLoading(false);
    }
  }, [atorId]);

  // Efeito que chama a busca de tarefas quando o atorId muda
  useEffect(() => {
    fetchTarefas();
  }, [fetchTarefas]);

  // Função para remover uma tarefa
  const removerTarefa = async (tarefaId: number): Promise<boolean> => {
    try {
      await deleteTarefaService(tarefaId);
      // Atualiza a lista localmente para refletir a remoção imediatamente
      setTarefas((prev) => prev.filter((t) => t.id !== tarefaId));
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao remover tarefa.");
      return false;
    }
  };

  // Retorna o estado e as funções para serem usadas nos componentes
  return { tarefas, loading, error, refetch: fetchTarefas, removerTarefa };
};
