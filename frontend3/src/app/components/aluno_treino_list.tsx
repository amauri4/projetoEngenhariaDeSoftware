"use client";
import { Treino } from "@/app/types/treino";
import { Ocorrencia } from "@/app/types/ocorrencia";
import { useState, useMemo, useEffect } from "react";
import { getOcorrenciasTreinoPorDataService, updateOcorrenciaTreinoStatusService } from "@/app/services/ocorrencia_treino_service";
import { TreinoDetailsModal } from "@/app/components/treino_details";
import { isBefore, parseISO, format, startOfYear, endOfYear } from "date-fns";

interface Props {
  treinos: Treino[]; 
  atorId: number;
}

export default function AlunoTreinoList({ treinos, atorId }: Props) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTreino, setSelectedTreino] = useState<Treino | null>(null);
  const [ocorrencias, setOcorrencias] = useState<Map<string, Ocorrencia>>(new Map());
  const [loadingOcorrencias, setLoadingOcorrencias] = useState(true);
  const [errorOcorrencias, setErrorOcorrencias] = useState<string | null>(null);

  useEffect(() => {
    const fetchTodasOcorrencias = async () => {
      if (!atorId || treinos.length === 0) {
        setLoadingOcorrencias(false);
        return;
      }
      
      const instrutorId = treinos[0].criador_id;
      if (!instrutorId) return;

      setLoadingOcorrencias(true);
      try {
        const hoje = new Date();
        const inicioDoAno = format(startOfYear(hoje), "yyyy-MM-dd");
        const fimDoAno = format(endOfYear(hoje), "yyyy-MM-dd");
        
        const data = await getOcorrenciasTreinoPorDataService(instrutorId, inicioDoAno, fimDoAno);
        
        const mapaOcorrencias = new Map(data.map(o => [`${o.treino_id}-${o.data}`, o]));
        setOcorrencias(mapaOcorrencias);
      } catch (error) {
        setErrorOcorrencias("Não foi possível carregar o status dos treinos.");
      } finally {
        setLoadingOcorrencias(false);
      }
    };
    fetchTodasOcorrencias();
  }, [atorId, treinos]);

  const treinosValidos = useMemo(() => {
    const hoje = new Date();
    return treinos.filter(treino => {
      if (!treino.data_entrega) return true; 
      const entrega = parseISO(`${treino.data_entrega}T23:59:59`); 
      return isBefore(hoje, entrega);
    });
  }, [treinos]);

  const handleToggleComplete = async (treinoId: number) => {
    const hojeFormatado = format(new Date(), 'yyyy-MM-dd');
    const ocorrenciaKey = `${treinoId}-${hojeFormatado}`;
    const ocorrencia = ocorrencias.get(ocorrenciaKey);

    if (!ocorrencia) {
      alert("Este treino não tem uma ocorrência para a data de hoje.");
      return;
    }

    try {
      const novoStatus = !ocorrencia.status;
      const ocorrenciaAtualizada = await updateOcorrenciaTreinoStatusService(ocorrencia.id, novoStatus);
      setOcorrencias(prev => new Map(prev).set(ocorrenciaKey, ocorrenciaAtualizada));
    } catch (error) {
      console.error("Erro ao atualizar treino:", error);
      alert("Não foi possível atualizar o status do treino.");
    }
  };

  const openModal = (treino: Treino) => {
    setSelectedTreino(treino);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedTreino(null);
  };

  if (treinos.length === 0) {
    return <p className="text-sm text-gray-500 mt-6">Nenhum treino atribuído a você.</p>;
  }
  
  if (treinosValidos.length === 0) {
    return <p className="text-sm text-gray-500 mt-6">Todos os seus treinos já foram concluídos.</p>;
  }

  return (
    <>
      <ul className="space-y-3 mt-6">
        {treinosValidos.map((treino) => {
          const hojeFormatado = format(new Date(), 'yyyy-MM-dd');
          const ocorrenciaKey = `${treino.id}-${hojeFormatado}`;
          const isCompleted = ocorrencias.get(ocorrenciaKey)?.status || false;

          return (
            <li 
              key={treino.id} 
              className="flex items-center bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
              onClick={() => openModal(treino)}
            >
              <input
                type="checkbox"
                checked={isCompleted}
                disabled={!ocorrencias.has(ocorrenciaKey)}
                onChange={(e) => {
                  e.stopPropagation();
                  handleToggleComplete(treino.id);
                }}
                className="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 mr-4 disabled:opacity-50"
              />
              <div className="flex-1">
                <p className={`font-medium ${isCompleted ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                  {treino.descricao}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  Data de Entrega: {treino.data_entrega ? new Date(`${treino.data_entrega}T00:00:00`).toLocaleDateString() : 'Não definido'}
                </p>
              </div>
            </li>
          );
        })}
      </ul>

      <TreinoDetailsModal
        isOpen={isModalOpen}
        onClose={closeModal}
        treino={selectedTreino}
        userType="aluno"
        selectedDate={selectedTreino?.data_entrega ? new Date(`${selectedTreino.data_entrega}T00:00:00`) : undefined} 
      />
    </>
  );
}
