"use client";

import { useState, useEffect, useCallback } from 'react';
import { Aluno } from '@/app/types/aluno';
import { getAlunosByInstrutor } from '@/app/services/alunos_instrutor_service';

export const useAlunos = (instrutor_id: number | null) => {
    const [alunos, setAlunos] = useState<Aluno[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchAlunos = useCallback(async () => {
        if (!instrutor_id) {
            setLoading(false);
            setAlunos([]); 
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const data = await getAlunosByInstrutor(instrutor_id);
            setAlunos(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Erro desconhecido ao buscar equipe.");
        } finally {
            setLoading(false);
        }
    }, [instrutor_id]); 

    useEffect(() => {
        fetchAlunos();
    }, [fetchAlunos]);

    return { alunos, loading, error, refetch: fetchAlunos };
};
