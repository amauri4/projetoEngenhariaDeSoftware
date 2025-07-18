"use client";

import { useState, useEffect, useCallback } from "react";
import { Treino } from "@/app/types/treino";
import { getTreinosPorAtorService, deleteTreinoService } from "@/app/services/treino_service";

export const useTreinos = (atorId: number | null) => {
  const [treinos, setTreinos] = useState<Treino[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTreinos = useCallback(async () => {
    if (!atorId) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await getTreinosPorAtorService(atorId);
      setTreinos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar treinos.");
    } finally {
      setLoading(false);
    }
  }, [atorId]);

  useEffect(() => {
    fetchTreinos();
  }, [fetchTreinos]);

  const removerTreino = async (treinoId: number): Promise<boolean> => {
    try {
      await deleteTreinoService(treinoId);
      setTreinos((prev) => prev.filter((t) => t.id !== treinoId));
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao remover treino.");
      return false;
    }
  };
  
  const adicionarTreinoLocalmente = (novoTreino: Treino) => {
    setTreinos((prev) => [...prev, novoTreino]);
  };

  return { treinos, loading, error, refetch: fetchTreinos, removerTreino, adicionarTreinoLocalmente };
};