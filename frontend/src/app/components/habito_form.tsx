"use client";

import { useState } from "react";

export interface HabitFormProps {
  onAdd: (habit: string) => void;
}

export default function HabitForm({ onAdd }: HabitFormProps) {
  const [habit, setHabit] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!habit.trim()) return;
    onAdd(habit);
    setHabit("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mt-4">
      <input
        value={habit}
        onChange={(e) => setHabit(e.target.value)}
        placeholder="Novo hábito"
        className="flex-1 p-2 border border-gray-300 rounded-lg"
      />
      <button
        type="submit"
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
      >
        Adicionar
      </button>
    </form>
  );
}
