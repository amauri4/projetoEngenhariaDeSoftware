"use client";

import { useState } from "react";
import { format } from "date-fns";
import HabitForm from "@/app/components/habito_form";
import HabitCalendar from "@/app/components/habito_calendar";
import HabitList from "@/app/components/habito_listas";

export default function HabitsDashboardPage() {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [habits, setHabits] = useState<string[]>([]);

  const handleAddHabit = (habit: string) => {
    setHabits((prev) => [...prev, habit]);
  };

  const handleDeleteHabit = (index: number) => {
    setHabits((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-indigo-500 to-purple-600 p-6">
      <main className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-indigo-700 mb-4">
          Painel de Hábitos
        </h1>

        <section className="mb-8">
          <HabitCalendar selectedDate={selectedDate} onDateChange={setSelectedDate} />
        </section>

        <section className="mb-8 mt-6"> 
          <HabitForm onAdd={handleAddHabit} />
        </section>

        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Hábitos em {format(selectedDate, 'dd/MM/yyyy')}
          </h2>
          <HabitList habits={habits} onRemove={handleDeleteHabit} />
        </section>

        <section className="mt-10 border-t pt-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Visualização Gráfica (Em breve)
          </h2>
          <div className="h-32 bg-gray-100 border border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-400">
            Gráficos e estatísticas de hábitos serão exibidos aqui.
          </div>
        </section>
      </main>
    </div>
  );
}
