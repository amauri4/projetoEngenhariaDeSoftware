"use client";

import { useState, useEffect, useCallback } from 'react';
import { Funcionario } from '@/app/types/funcionario';
import { getEquipeByGerenteService } from '@/app/services/equipe_gerente_service';

export const useFuncionarios = (gerenteId: number | null) => {
    const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchEquipe = useCallback(async () => {
        if (!gerenteId) {
            setLoading(false);
            setFuncionarios([]); 
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const data = await getEquipeByGerenteService(gerenteId);
            setFuncionarios(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Erro desconhecido ao buscar equipe.");
        } finally {
            setLoading(false);
        }
    }, [gerenteId]); 

    useEffect(() => {
        fetchEquipe();
    }, [fetchEquipe]);

    return { funcionarios, loading, error, refetch: fetchEquipe };
};
