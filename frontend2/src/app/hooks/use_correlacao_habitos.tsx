import { useState } from 'react';
import { buscarCorrelacoesHabitos } from '@/app/services/correlacao_habitos';

export const useCorrelacoes = () => {
  const [correlacoes, setCorrelacoes] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const buscarCorrelacoes = async (usuarioId: number) => {
    try {
      setLoading(true);
      setError(null);
      const resultado = await buscarCorrelacoesHabitos(usuarioId);
      setCorrelacoes(resultado);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
      setCorrelacoes('');
    } finally {
      setLoading(false);
    }
  };

  return {
    correlacoes,
    loading,
    error,
    buscarCorrelacoes,
  };
};