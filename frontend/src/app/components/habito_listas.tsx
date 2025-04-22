"use client";

import type { HabitoUsuario } from "@/app/types/habito_usuario";
import { useHabits } from "@/app/hooks/use_lista_habitos";
import useDeleteHabit from "@/app/hooks/use_remove_habitos";

export interface HabitListProps {
  habits: HabitoUsuario[];
  onRemove: (idRemovido: number) => void; // notifica o pai opcionalmente
}

export default function HabitList({ habits, onRemove }: HabitListProps) {
  const { habits: availableHabits } = useHabits();
  const { deleteHabit, loadingDeleteHabit } = useDeleteHabit();

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

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Seus hábitos do dia</h2>
      {habits.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhum hábito adicionado.</p>
      ) : (
        <ul className="space-y-2">
          {habits.map((habit) => (
            <li
              key={habit.id}
              className="flex justify-between items-center bg-gray-100 p-2 rounded-lg"
            >
              <span>{habitNamesMap.get(habit.habito_base_id) ?? "Hábito desconhecido"}</span>
              <span>{habit.descricao ?? ""}</span>
              <button
                onClick={() => handleRemove(habit)}
                disabled={loadingDeleteHabit}
                className="text-red-500 hover:underline text-sm disabled:opacity-50"
              >
                {loadingDeleteHabit ? "Removendo..." : "Remover"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
