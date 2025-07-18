"use client";

import { Tarefa } from "@/app/types/tarefa";
import { Ocorrencia } from "@/app/types/ocorrencia";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment, useState, useEffect } from "react";
import { format } from "date-fns";
import { getOcorrenciasPorDataEspecificaService, updateOcorrenciaStatusService } from "@/app/services/ocorrencia_tarefa_service";
import { useAuth } from "@/app/hooks/use_auth";

type UserRole = 'gerente' | 'funcionario';

interface TarefaDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  tarefa: Tarefa | null;
  userType: UserRole;
  selectedDate?: Date; 
}

export function TarefaDetailsModal({
  isOpen,
  onClose,
  tarefa,
  userType,
  selectedDate,
}: TarefaDetailsModalProps) {
  const { id: atorId } = useAuth();
  const [isCompleted, setIsCompleted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [ocorrencia, setOcorrencia] = useState<Ocorrencia | null>(null);

  useEffect(() => {
    const fetchCompletionStatus = async () => {
      if (!tarefa || !isOpen || !atorId || userType !== 'funcionario' || !selectedDate) {
        setOcorrencia(null);
        setIsCompleted(false);
        return;
      }

      try {
        setLoading(true);
        const dataFormatada = format(selectedDate, 'yyyy-MM-dd');
        const registros = await getOcorrenciasPorDataEspecificaService(tarefa.criador_id, dataFormatada);

        const registroAtual = registros.find(r => r.tarefa_id === tarefa.id);
        
        if (registroAtual) {
          setOcorrencia(registroAtual);
          setIsCompleted(registroAtual.status);
        } else {
          setOcorrencia(null);
          setIsCompleted(false);
        }
      } catch (error) {
        console.error("Erro ao verificar status da tarefa:", error);
        setOcorrencia(null);
        setIsCompleted(false);
      } finally {
        setLoading(false);
      }
    };

    fetchCompletionStatus();
  }, [tarefa, selectedDate, isOpen, atorId, userType]);

  const handleToggleComplete = async () => {
    if (loading || !ocorrencia) return;

    try {
      setLoading(true);
      const novoStatus = !isCompleted;
      const ocorrenciaAtualizada = await updateOcorrenciaStatusService(ocorrencia.id, novoStatus);
      setOcorrencia(ocorrenciaAtualizada);
      setIsCompleted(ocorrenciaAtualizada.status);
    } catch (error) {
      console.error("Erro ao atualizar status da tarefa:", error);
      alert("Não foi possível atualizar o status da tarefa.");
    } finally {
      setLoading(false);
    }
  };

  if (!tarefa) return null;

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
                  Detalhes da Tarefa
                </Dialog.Title>

                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-700">Descrição:</h4>
                    <p>{tarefa.descricao || "Nenhuma descrição fornecida"}</p>
                  </div>

                  {/* Mostra o responsável (visão do gerente) */}
                  {userType === 'gerente' && (
                    <div>
                      <h4 className="font-semibold text-gray-700">Responsável:</h4>
                      <p>{tarefa.responsavel_nome || "Não atribuído"}</p>
                    </div>
                  )}

                  <div>
                    <h4 className="font-semibold text-gray-700">Prazo Final:</h4>
                    <p>{tarefa.prazo_final ? new Date(`${tarefa.prazo_final}T00:00:00`).toLocaleDateString() : "Não definido"}</p>
                  </div>

                  {/* Lógica de conclusão (visão do funcionário) */}
                  {userType === 'funcionario' && selectedDate && (
                    <div className="flex items-center pt-2">
                      <input
                        type="checkbox"
                        id="completed-checkbox"
                        checked={isCompleted}
                        onChange={handleToggleComplete}
                        disabled={loading || !ocorrencia}
                        className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50"
                      />
                      <label htmlFor="completed-checkbox" className="ml-3 block text-sm text-gray-900">
                        {loading ? "Carregando..." :
                          !ocorrencia ? `Tarefa não agendada para ${format(selectedDate, 'dd/MM/yyyy')}` : `Concluído em ${format(selectedDate, 'dd/MM/yyyy')}`}
                      </label>
                    </div>
                  )}
                </div>

                <div className="mt-6">
                  <button
                    type="button"
                    className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
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
