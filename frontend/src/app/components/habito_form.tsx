"use client";

import { useEffect, useState } from "react";
import type { HabitoBase } from "@/app/types/habito_base";
import { HabitoUsuario } from "../types/habito_usuario";

export interface HabitFormProps {
  availableHabits: HabitoBase[];
  onAdd: (habitoBaseId: number | null, descricao: string | null) => Promise<HabitoUsuario | null>;
  onAddedSuccessfully?: () => void;
}

export default function HabitForm({ onAdd, availableHabits }: HabitFormProps) {
  const [selectedHabitId, setSelectedHabitId] = useState<number | null>(null);
  const [descricao, setDescricao] = useState("");
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [erro, setErro] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const habit = availableHabits.find((h) => h.id === selectedHabitId);
    if (!habit || !descricao.trim()) {
      setErro("Por favor, preencha todos os campos.");
      setMensagem(null);
      return;
    }

    try {
      await onAdd(habit.id, descricao.trim());
      setMensagem("Hábito adicionado com sucesso!");
      setErro(null);
      setDescricao("");
      setSelectedHabitId(null);
    } catch (error: any) {
      setErro("Erro ao adicionar hábito.");
      setMensagem(null);
    }
  };

  useEffect(() => {
    if (mensagem) {
      const timer = setTimeout(() => {
        setMensagem(null);
      }, 3000);

      return () => clearTimeout(timer); 
    }
  }, [mensagem]);

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 mt-4">
      <select
        value={selectedHabitId ?? ""}
        onChange={(e) => setSelectedHabitId(Number(e.target.value))}
        className="p-2 border border-gray-300 rounded-lg"
      >
        <option value="">Selecione um hábito</option>
        {availableHabits.map((habit) => (
          <option key={habit.id} value={habit.id}>
            {habit.nome}
          </option>
        ))}
      </select>

      <textarea
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
        placeholder="Descrição do hábito (até 255 caracteres)"
        maxLength={255}
        className="p-2 border border-gray-300 rounded-lg resize-none"
      />

      <button
        type="submit"
        disabled={!selectedHabitId || !descricao.trim()}
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
      >
        Adicionar
      </button>

      {mensagem && <p className="text-green-600">{mensagem}</p>}
      {erro && <p className="text-red-600">{erro}</p>}
    </form>
  );
}
