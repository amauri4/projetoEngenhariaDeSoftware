"use client";

import type { Habito } from "@/app/types/habit";
import useHabitNameById from "../utils/id_para_nome";

export interface HabitListProps {
  habits: Habito[];
  onRemove: (index: number) => void;
}

export default function HabitList({ habits, onRemove }: HabitListProps) {
  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Seus hábitos do dia</h2>
      {habits.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhum hábito adicionado.</p>
      ) : (
        <ul className="space-y-2">
          {habits.map((habit, index) => (
            <li
              key={habit.id}
              className="flex justify-between items-center bg-gray-100 p-2 rounded-lg"
            >
              <span>{useHabitNameById(habit.id)}</span>
              <button
                onClick={() => onRemove(index)}
                className="text-red-500 hover:underline text-sm"
              >
                Remover
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
