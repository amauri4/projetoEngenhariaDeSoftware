"use client";

import { useEffect, useState } from "react";
import { format } from "date-fns";

import HabitForm from "@/app/components/habito_form";
import HabitCalendar from "@/app/components/habito_calendar";
import HabitList from "@/app/components/habito_listas";

import { useHabits as listar_habitos } from "@/app/hooks/use_lista_habitos";
import { useHabitosUsuario } from "@/app/hooks/use_habitos_usuarios";
import useAddHabit from "@/app/hooks/use_add_habitos";
import { HabitoUsuario } from "../types/habito_usuario";

export default function HabitsDashboardPage() {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [habits, setHabits] = useState<HabitoUsuario[]>([]); 
  const [usuarioId, setUsuarioId] = useState<number | null>(null);
  const { habits: availableHabits, loading, error } = listar_habitos();
  const { addHabit, loadingHabit, errorHabit } = useAddHabit(usuarioId);
  const [refreshKey, setRefreshKey] = useState(0);
  const { habitsUsuario, loadingUsuario, errorUsuario } = useHabitosUsuario(usuarioId, refreshKey);

  useEffect(() => {
    const usuarioIdString = typeof window !== "undefined" ? localStorage.getItem("usuario_id") : null;
    const parsedId = usuarioIdString ? parseInt(usuarioIdString, 10) : null;
    if (parsedId && !isNaN(parsedId)) {
      setUsuarioId(parsedId);
    }
  }, []);

  useEffect(() => {
    if (habitsUsuario && habitsUsuario.length > 0) {
      setHabits(habitsUsuario);
    } 
  }, [habitsUsuario, refreshKey]);

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
          <HabitForm 
            onAdd={addHabit} 
            availableHabits={availableHabits} 
            onAddedSuccessfully={() => {
              setHabits((prev) => [...prev, ...habitsUsuario]);
              setRefreshKey((prev) => prev + 1);
            }}
          />

          {loading && <p>Carregando hábitos disponíveis...</p>}
          {error && <p className="text-red-500">Erro ao carregar hábitos: {error}</p>}
          {loadingUsuario && <p>Carregando hábitos do usuário...</p>}
          {errorUsuario && <p className="text-red-500"> {errorUsuario}</p>}
          {loadingHabit && <p>Adicionando hábito...</p>}
          {errorHabit && <p className="text-red-500">Erro ao adicionar hábito: {errorHabit}</p>}
        </section>

        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">
            Hábitos em {format(selectedDate, "dd/MM/yyyy")}
          </h2>
          <HabitList
            habits={habits}
            onRemove={(idRemovido) => {
              setHabits((prev) => prev.filter((h) => h.id !== idRemovido));
            }}
          />
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
