"use client";
import { Tarefa } from "@/app/types/tarefa";
import { useMemo, useState } from "react";
import { TarefaDetailsModal } from "@/app/components/tarefa_details";

interface Props {
  tarefas: Tarefa[];
}

export default function GerenteTarefaList({ tarefas }: Props) {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedTarefa, setSelectedTarefa] = useState<Tarefa | null>(null);

    const tarefasAgrupadas = useMemo(() => {
    return tarefas.reduce((acc, tarefa) => {
      const responsavelNome = tarefa.responsavel_nome || "Não Atribuído";
      if (!acc[responsavelNome]) {
        acc[responsavelNome] = [];
      }
      acc[responsavelNome].push(tarefa);
      return acc;
    }, {} as Record<string, Tarefa[]>);
  }, [tarefas]);

  const openModal = (tarefa: Tarefa) => {
    setSelectedTarefa(tarefa);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedTarefa(null);
  };

  if (tarefas.length === 0) {
    return <p className="text-sm text-gray-500">Nenhuma tarefa criada ainda.</p>;
  }

  return (
    <>
      <div className="space-y-6 mt-6">
        {Object.entries(tarefasAgrupadas).map(([responsavel, listaDeTarefas]) => (
          <div key={responsavel}>
            <h3 className="font-bold text-lg text-gray-700 border-b pb-2 mb-3">{responsavel}</h3>
            <ul className="space-y-3">
              {listaDeTarefas.map((tarefa) => (
                <li 
                  key={tarefa.id} 
                  className="bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
                  onClick={() => openModal(tarefa)}
                >
                  <p className="font-medium text-gray-800">{tarefa.descricao}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    Prazo: {tarefa.prazo_final ? new Date(`${tarefa.prazo_final}T00:00:00`).toLocaleDateString()  : 'Não definido'}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <TarefaDetailsModal
        isOpen={isModalOpen}
        onClose={closeModal}
        tarefa={selectedTarefa}
        userType="gerente"
      />
    </>
  );
}