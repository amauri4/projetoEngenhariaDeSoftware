"use client";

import type { HabitoUsuario } from "@/app/types/habito_usuario";
import { useHabits } from "@/app/hooks/use_lista_habitos";
import useDeleteHabit from "@/app/hooks/use_remove_habitos";
import { useState } from "react";
import { HabitDetailsModal } from "@/app/components/habit_details";
import { format, isSameDay } from "date-fns";
import { Frequencia } from "@/app/types/frequencia";

export interface HabitListProps {
  habits: HabitoUsuario[];
  onRemove: (idRemovido: number) => void;
  selectedDate: Date;
}

export default function HabitList({ habits, onRemove, selectedDate }: HabitListProps) {
  const { habits: availableHabits } = useHabits();
  const { deleteHabit, loadingDeleteHabit } = useDeleteHabit();
  const [selectedHabit, setSelectedHabit] = useState<HabitoUsuario | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const habitNamesMap = new Map<number, string>();
  availableHabits?.forEach((habit) => {
    habitNamesMap.set(habit.id, habit.nome);
  });

  const handleRemove = async (habit: HabitoUsuario) => {
    if (!habit.id) {
      console.error("Hábito sem ID, impossível remover.");
      return;
    }

    const sucesso = await deleteHabit(habit.id);
    if (sucesso) {
      onRemove(habit.id);
    } else {
      console.error("Erro ao remover hábito.");
    }
  };

  const openHabitDetails = (habit: HabitoUsuario) => {
    setSelectedHabit(habit);
    setIsModalOpen(true);
  };

  const filteredHabits = habits.filter(habit => {
    const habitStartDate = new Date(habit.data_inicio);

    if (habitStartDate > selectedDate) return false;

    switch (habit.frequencia) {
      case Frequencia.DIARIA:
        return true;
      case Frequencia.SEMANAL:
        return habit.dias_semana?.includes(selectedDate.getDay()) ?? false;
      case Frequencia.MENSAL:
        return habit.dias_mes?.includes(selectedDate.getDate()) ?? false;
      default:
        return false;
    }
  });

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">
        Seus hábitos para {format(selectedDate, "dd/MM/yyyy")}
      </h2>
      
      {filteredHabits.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhum hábito para esta data.</p>
      ) : (
        <ul className="space-y-2">
          {filteredHabits.map((habit) => (
            <li
              key={habit.id}
              className="flex justify-between items-center bg-gray-100 p-3 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
              onClick={() => openHabitDetails(habit)}
            >
              <div className="flex-1">
                <h3 className="font-medium">
                  {habitNamesMap.get(habit.habito_base_id) ?? "Hábito desconhecido"}
                </h3>
                {habit.descricao && (
                  <p className="text-sm text-gray-600 truncate">{habit.descricao}</p>
                )}
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemove(habit);
                }}
                disabled={loadingDeleteHabit}
                className="ml-4 text-red-500 hover:text-red-700 text-sm disabled:opacity-50"
              >
                {loadingDeleteHabit ? "Removendo..." : "Remover"}
              </button>
            </li>
          ))}
        </ul>
      )}

      <HabitDetailsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        habit={selectedHabit}
      />
    </div>
  );
}
