"use client";
import { Tarefa } from "@/app/types/tarefa";
import { Ocorrencia } from "@/app/types/ocorrencia";
import { useState, useEffect, useMemo } from "react";
import { getOcorrenciasPorDataService, updateOcorrenciaStatusService } from "@/app/services/ocorrencia_tarefa_service";
import { format, startOfWeek, endOfWeek, startOfMonth, endOfMonth, startOfYear, endOfYear, isWithinInterval, parseISO, Interval } from "date-fns";
import { TarefaDetailsModal } from "@/app/components/tarefa_details";

type FiltroPeriodo = 'hoje' | 'semana' | 'mes' | 'ano';

interface Props {
  tarefas: Tarefa[]; 
  atorId: number;
}

export default function FuncionarioTarefaList({ tarefas, atorId }: Props) {
  const [ocorrencias, setOcorrencias] = useState<Map<number, Ocorrencia>>(new Map());
  const [filtro, setFiltro] = useState<FiltroPeriodo>('hoje');
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTarefa, setSelectedTarefa] = useState<Tarefa | null>(null);

  useEffect(() => {
    const fetchTodasOcorrencias = async () => {
      setLoading(true);
      try {
        const hoje = new Date();
        const inicioDoAno = format(startOfYear(hoje), "yyyy-MM-dd");
        const fimDoAno = format(endOfYear(hoje), "yyyy-MM-dd");
        const data = await getOcorrenciasPorDataService(atorId, inicioDoAno, fimDoAno);
        const mapaOcorrencias = new Map(data.map(o => [o.tarefa_id, o]));
        setOcorrencias(mapaOcorrencias);
      } catch (error) {
        //console.error("Erro ao buscar ocorrências:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTodasOcorrencias();
  }, [atorId]);

  const tarefasFiltradas = useMemo(() => {
    const hoje = new Date();
    let intervalo: Interval;

    if (filtro === 'hoje') {
      intervalo = { start: hoje, end: hoje };
    } else if (filtro === 'semana') {
      intervalo = { start: startOfWeek(hoje, { weekStartsOn: 1 }), end: endOfWeek(hoje, { weekStartsOn: 1 }) };
    } else if (filtro === 'mes') {
      intervalo = { start: startOfMonth(hoje), end: endOfMonth(hoje) };
    } else { 
      intervalo = { start: startOfYear(hoje), end: endOfYear(hoje) };
    }

    return tarefas.filter(tarefa => {
      if (!tarefa.prazo_final) return false;
      const prazo = new Date(`${tarefa.prazo_final}T00:00:00`);
      return isWithinInterval(prazo, intervalo);
    });
  }, [tarefas, filtro]);

  const handleToggleComplete = async (tarefaId: number) => {
    const ocorrencia = ocorrencias.get(tarefaId);
    if (!ocorrencia) {
      alert("Não foi possível encontrar o registro de ocorrência para esta tarefa.");
      return;
    }

    try {
      const novoStatus = !ocorrencia.status;
      const ocorrenciaAtualizada = await updateOcorrenciaStatusService(ocorrencia.id, novoStatus);
      
      setOcorrencias(prev => new Map(prev).set(tarefaId, ocorrenciaAtualizada));
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
      alert("Não foi possível atualizar o status da tarefa.");
    }
  };

  const openModal = (tarefa: Tarefa) => {
    setSelectedTarefa(tarefa);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedTarefa(null);
  };

  return (
    <>
      <div className="flex space-x-2 border-b pb-2 mb-4">
        {(['hoje', 'semana', 'mes', 'ano'] as FiltroPeriodo[]).map((periodo) => (
          <button
            key={periodo}
            onClick={() => setFiltro(periodo)}
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${
              filtro === periodo
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {periodo.charAt(0).toUpperCase() + periodo.slice(1)}
          </button>
        ))}
      </div>

      {loading && <p>Buscando dados...</p>}
      {!loading && tarefasFiltradas.length === 0 && (
        <p className="text-sm text-gray-500 mt-6">Nenhuma tarefa com prazo para este período.</p>
      )}
      
      {!loading && (
        <ul className="space-y-3 mt-6">
          {tarefasFiltradas.map((tarefa) => {
            const isCompleted = ocorrencias.get(tarefa.id)?.status || false;
            return (
              <li 
                key={tarefa.id} 
                className="flex items-center bg-gray-100 p-4 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
                onClick={() => openModal(tarefa)}
              >
                <input
                  type="checkbox"
                  checked={isCompleted}
                  disabled={!ocorrencias.has(tarefa.id)}
                  onChange={(e) => {
                    e.stopPropagation();
                    handleToggleComplete(tarefa.id);
                  }}
                  className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-4 disabled:opacity-50"
                />
                <div className="flex-1">
                  <p className={`font-medium ${isCompleted ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                    {tarefa.descricao}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                  Prazo: {tarefa.prazo_final ? new Date(`${tarefa.prazo_final}T00:00:00`).toLocaleDateString() : 'Não definido'}
                  </p>
                </div>
              </li>
            );
          })}
        </ul>
      )}

      <TarefaDetailsModal
        isOpen={isModalOpen}
        onClose={closeModal}
        tarefa={selectedTarefa}
        userType="funcionario"
        selectedDate={selectedTarefa?.prazo_final ? new Date(`${selectedTarefa.prazo_final}T00:00:00`) : undefined} 
      />
    </>
  );
}
