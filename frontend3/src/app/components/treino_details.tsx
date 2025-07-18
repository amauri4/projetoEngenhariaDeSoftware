"use client";

import { Treino } from "@/app/types/treino";
import { Ocorrencia } from "@/app/types/ocorrencia";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment, useState, useEffect } from "react";
import { format } from "date-fns";
import { getOcorrenciasPorDataEspecificaService, updateOcorrenciaTreinoStatusService } from "@/app/services/ocorrencia_treino_service";
import { useAuth } from "@/app/hooks/use_auth";

type UserRole = 'instrutor' | 'aluno';

interface TreinoDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  treino: Treino | null;
  userType: UserRole;
  selectedDate?: Date; 
}

export function TreinoDetailsModal({
  isOpen,
  onClose,
  treino,
  userType,
  selectedDate,
}: TreinoDetailsModalProps) {
  const { id: atorId } = useAuth();
  const [isCompleted, setIsCompleted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [ocorrencia, setOcorrencia] = useState<Ocorrencia | null>(null);

  useEffect(() => {
    const fetchCompletionStatus = async () => {
      if (!treino || !isOpen || !atorId || userType !== 'aluno' || !selectedDate) {
        setOcorrencia(null);
        setIsCompleted(false);
        return;
      }

      try {
        setLoading(true);
        const dataFormatada = format(selectedDate, 'yyyy-MM-dd');
        // --- MODIFICAÇÃO: A busca de ocorrências agora usa o ID do criador do treino (o instrutor) ---
        // Isso alinha a lógica com o exemplo funcional fornecido (TarefaDetailsModal).
        const registros = await getOcorrenciasPorDataEspecificaService(treino.criador_id, dataFormatada);
        
        const registroAtual = registros.find(r => r.treino_id === treino.id);
        
        if (registroAtual) {
          setOcorrencia(registroAtual);
          setIsCompleted(registroAtual.status);
        } else {
          setOcorrencia(null);
          setIsCompleted(false);
        }
      } catch (error) {
        console.error("Erro ao verificar status do treino:", error);
        setOcorrencia(null);
        setIsCompleted(false);
      } finally {
        setLoading(false);
      }
    };

    fetchCompletionStatus();
  }, [treino, selectedDate, isOpen, atorId, userType]);

  const handleToggleComplete = async () => {
    if (loading || !ocorrencia) return;

    try {
      setLoading(true);
      const novoStatus = !isCompleted;
      const ocorrenciaAtualizada = await updateOcorrenciaTreinoStatusService(ocorrencia.id, novoStatus);
      setOcorrencia(ocorrenciaAtualizada);
      setIsCompleted(ocorrenciaAtualizada.status);
    } catch (error) {
      console.error("Erro ao atualizar status do treino:", error);
      alert("Não foi possível atualizar o status do treino.");
    } finally {
      setLoading(false);
    }
  };

  if (!treino) return null;

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100"
          leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/30 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300" enterFrom="opacity-0 scale-95" enterTo="opacity-100 scale-100"
              leave="ease-in duration-200" leaveFrom="opacity-100 scale-100" leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                  Detalhes do Treino
                </Dialog.Title>

                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-700">Descrição:</h4>
                    <p>{treino.descricao || "Nenhuma descrição fornecida"}</p>
                  </div>

                  {userType === 'instrutor' && (
                    <div>
                      <h4 className="font-semibold text-gray-700">Aluno:</h4>
                      <p>{treino.responsavel_nome || "Não atribuído"}</p>
                    </div>
                  )}
                  
                  {userType === 'aluno' && (
                    <div>
                      <h4 className="font-semibold text-gray-700">Instrutor:</h4>
                      <p>{treino.criador_nome || "Não atribuído"}</p>
                    </div>
                  )}

                  <div>
                    <h4 className="font-semibold text-gray-700">Data de Início:</h4>
                    <p>{treino.data_inicio ? new Date(`${treino.data_inicio}T00:00:00`).toLocaleDateString() : "Não definida"}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-700">Data de Entrega:</h4>
                    <p>{treino.data_entrega ? new Date(`${treino.data_entrega}T00:00:00`).toLocaleDateString() : "Não definido"}</p>
                  </div>

                  {userType === 'aluno' && selectedDate && (
                    <div className="flex items-center pt-2">
                      <input
                        type="checkbox"
                        id="completed-checkbox"
                        checked={isCompleted}
                        onChange={handleToggleComplete}
                        disabled={loading || !ocorrencia}
                        className="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 disabled:opacity-50"
                      />
                      <label htmlFor="completed-checkbox" className="ml-3 block text-sm text-gray-900">
                        {loading ? "Carregando..." :
                          !ocorrencia ? `Treino não agendado para ${format(selectedDate, 'dd/MM/yyyy')}` : `Concluído em ${format(selectedDate, 'dd/MM/yyyy')}`}
                      </label>
                    </div>
                  )}
                </div>

                <div className="mt-6">
                  <button
                    type="button"
                    className="inline-flex justify-center rounded-md border border-transparent bg-orange-100 px-4 py-2 text-sm font-medium text-orange-900 hover:bg-orange-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2"
                    onClick={onClose}
                  >
                    Fechar
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition>
  );
}
