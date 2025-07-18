"use client";

import type { Tarefa } from "@/app/types/tarefa";
import { useState } from "react";

export interface TarefaListProps {
  tarefas: Tarefa[];
  onRemove: (idRemovido: number) => Promise<boolean>;
}

export default function TarefaList({ tarefas, onRemove }: TarefaListProps) {
  const [loadingRemoveId, setLoadingRemoveId] = useState<number | null>(null);

  const handleRemove = async (tarefa: Tarefa) => {
    if (!tarefa.id) return;
    setLoadingRemoveId(tarefa.id);
    await onRemove(tarefa.id);
    setLoadingRemoveId(null);
  };

  return (
    <div className="mt-6">
      {tarefas.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhuma tarefa encontrada para esta equipe.</p>
      ) : (
        <ul className="space-y-3">
          {tarefas.map((tarefa) => (
            <li
              key={tarefa.id}
              className="flex justify-between items-center bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <div className="flex-1">
                <h3 className="font-medium text-gray-800">{tarefa.descricao}</h3>
                <div className="text-sm text-gray-600 mt-1">
                  <span>Responsável: <strong>{tarefa.responsavel_nome ?? 'N/A'}</strong></span>
                  <span className="mx-2">|</span>
                  <span>Prazo: <strong>{tarefa.prazo_final ? new Date(tarefa.prazo_final).toLocaleDateString() : 'Não definido'}</strong></span>
                </div>
              </div>
              
              <button
                onClick={() => handleRemove(tarefa)}
                disabled={loadingRemoveId === tarefa.id}
                className="ml-4 text-red-500 hover:text-red-700 text-sm disabled:opacity-50 font-semibold"
              >
                {loadingRemoveId === tarefa.id ? "Removendo..." : "Remover"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}