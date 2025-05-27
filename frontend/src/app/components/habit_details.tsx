"use client";

import { HabitoUsuario } from "@/app/types/habito_usuario";
import { Frequencia } from "@/app/types/frequencia";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment, useState, useEffect } from "react";
import { isSameDay } from "date-fns";
import { RegistroDiarioUpdateInput } from "../types/registro_habito";

interface HabitDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  habit: HabitoUsuario | null;
  selectedDate: Date;
  onToggleComplete: (registroId: number, data: RegistroDiarioUpdateInput) => Promise<void>;
  getRegistrosPorDataEspecifica: (usuarioId: number, date: string) => Promise<any[]>;
}

export function HabitDetailsModal({
  isOpen,
  onClose,
  habit,
  selectedDate,
  onToggleComplete,
  getRegistrosPorDataEspecifica
}: HabitDetailsModalProps) {
  const [isCompleted, setIsCompleted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [registroId, setRegistroId] = useState<number | null>(null);

  useEffect(() => {
    const fetchCompletionStatus = async () => {
      if (!habit || !isOpen) return;

      try {
        setLoading(true);
        const usuarioId = Number(localStorage.getItem('usuario_id'));
        const dataFormatada = selectedDate.toISOString().split('T')[0];
        const registros = await getRegistrosPorDataEspecifica(usuarioId, dataFormatada);

        const registro = registros.find(r => r.habito_id === habit.id);
        setIsCompleted(registro?.concluido || false);
        setRegistroId(registro?.id || null);
      } catch (error) {
        console.error("Erro ao verificar status do hábito:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCompletionStatus();
  }, [habit, selectedDate, isOpen]);

  const handleToggleComplete = async () => {
    if (!habit || loading || registroId === null) return;

    try {
      setLoading(true);
      const newStatus = !isCompleted;
      setIsCompleted(newStatus);
      const registroData: RegistroDiarioUpdateInput = {
        concluido: newStatus
      };
      await onToggleComplete(habit.id, registroData);
    } catch (error) {
      console.error("Erro ao atualizar status do hábito:", error);
    } finally {
      setLoading(false);
    }
  };

  const getFrequencyDetails = () => {
    if (!habit) return "Nenhum hábito selecionado";

    switch (habit.frequencia) {
      case Frequencia.DIARIA:
        const diasSemanaNumeros = (habit.dias_semana as unknown as string[]).map(dia => {
          if (!isNaN(Number(dia))) {
            return Number(dia);
          }

          const diaLower = dia.toString().toLowerCase().trim();
          const mapeamento: Record<string, number> = {
            'domingo': 0,
            'segunda': 1,
            'terça': 2,
            'quarta': 3,
            'quinta': 4,
            'sexta': 5,
            'sábado': 6
          };

          return mapeamento[diaLower] ?? 0;
        });

        const diaSelecionado = selectedDate.getDay();
        const diaAtivo = diasSemanaNumeros.includes(diaSelecionado);

        return `Diário (${diasSemanaNumeros.map(d => ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"][d]).join(", ")}) - ${diaAtivo ? "Ativo hoje" : "Inativo hoje"}`;

      case Frequencia.SEMANAL:
        return `${habit.vezes_na_semana} vezes na semana`;

      case Frequencia.MENSAL:
        const diaMesAtivo = habit.dias_mes?.includes(selectedDate.getDate()) ?? false;
        return `Dias ${habit.dias_mes?.join(", ")} do mês - ${diaMesAtivo ? "Ativo hoje" : "Inativo hoje"}`;

      default:
        return "Frequência não especificada";
    }
  };

  if (!habit) return null;

  return (
    <Transition appear show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-white/5 backdrop-blur-sm" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <Dialog.Title
                  as="h3"
                  className="text-lg font-medium leading-6 text-gray-900"
                >
                  Detalhes do Hábito
                </Dialog.Title>

                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="font-semibold">Descrição:</h4>
                    <p>{habit.descricao || "Nenhuma descrição fornecida"}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold">Frequência:</h4>
                    <p>{getFrequencyDetails()}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold">Data de início:</h4>
                    <p>{new Date(habit.data_inicio).toLocaleDateString()}</p>
                  </div>

                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="completed-checkbox"
                      checked={isCompleted}
                      onChange={handleToggleComplete}
                      disabled={loading || registroId === null}
                      className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <label htmlFor="completed-checkbox" className="ml-2 block text-sm text-gray-900">
                      {loading ? "Carregando..." :
                        registroId === null ? "Registro não encontrado" : "Concluído hoje"}
                    </label>
                  </div>
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