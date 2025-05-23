"use client";

import { HabitoUsuario } from "@/app/types/habito_usuario";
import { Frequencia } from "@/app/types/frequencia";
import { Dialog, Transition } from "@headlessui/react";
import { Fragment } from "react";

interface HabitDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  habit: HabitoUsuario | null;
}

export function HabitDetailsModal({ isOpen, onClose, habit }: HabitDetailsModalProps) {
  if (!habit) return null;

  const getFrequencyDetails = () => {
    switch (habit.frequencia) {
      case Frequencia.DIARIA:
        return "Todos os dias";
      case Frequencia.SEMANAL:
        return `${habit.vezes_na_semana} vezes na semana${habit.dias_semana?.length
          ? ` (${habit.dias_semana.map(d => ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"][d]).join(", ")})`
          : ""
          }`;
      case Frequencia.MENSAL:
        return `Dias ${habit.dias_mes?.join(", ")} do mês`;
      default:
        return "Frequência não especificada";
    }
  };

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