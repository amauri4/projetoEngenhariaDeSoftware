"use client";

import { useEffect, useState } from "react";
import type { HabitoBase } from "@/app/types/habito_base";
import useAddHabit from "@/app/hooks/use_add_habitos";
import { Frequencia } from "@/app/types/frequencia";

export interface HabitFormProps {
  availableHabits: HabitoBase[];
  onAdd: () => void;
  idUsuario: number | null;
}

export default function HabitForm({ onAdd, availableHabits, idUsuario }: HabitFormProps) {
  const [selectedHabitId, setSelectedHabitId] = useState<number | null>(null);
  const [descricao, setDescricao] = useState("");
  const [frequencia, setFrequencia] = useState<Frequencia>(Frequencia.DIARIA);
  const [dataInicio, setDataInicio] = useState<string>(new Date().toISOString().split('T')[0]);
  const [vezesNaSemana, setVezesNaSemana] = useState<number | null>(null);
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [erro, setErro] = useState<string | null>(null);

  const { addHabit, loadingHabit, errorHabit } = useAddHabit(idUsuario ?? 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (idUsuario === null) {
      setErro("Usuário não identificado.");
      return;
    }

    if (!selectedHabitId || !descricao.trim()) {
      setErro("Por favor, preencha todos os campos obrigatórios.");
      return;
    }

    if (frequencia === Frequencia.SEMANAL && !vezesNaSemana) {
      setErro("Para frequência semanal, informe quantas vezes na semana.");
      return;
    }

    try {
      await addHabit(
        selectedHabitId,
        descricao,
        frequencia,
        new Date(dataInicio),
        frequencia === Frequencia.SEMANAL ? vezesNaSemana : null
      );
      
      onAdd();
      setMensagem("Hábito adicionado com sucesso!");
      resetForm();
    } catch (error) {
      console.error(error);
      setErro(error instanceof Error ? error.message : "Erro ao adicionar hábito.");
    }
  };

  const resetForm = () => {
    setDescricao("");
    setSelectedHabitId(null);
    setFrequencia(Frequencia.DIARIA);
    setDataInicio("");
    setVezesNaSemana(null);
    setErro(null);
  };

  useEffect(() => {
    if (mensagem) {
      const timer = setTimeout(() => setMensagem(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [mensagem]);

  useEffect(() => {
    if (frequencia !== Frequencia.SEMANAL) {
      setVezesNaSemana(null);
    }
  }, [frequencia]);

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 mt-4">
      {/* Seleção de hábito */}
      <select
        value={selectedHabitId ?? ""}
        onChange={(e) => setSelectedHabitId(Number(e.target.value))}
        className="p-2 border border-gray-300 rounded-lg"
        required
      >
        <option value="">Selecione um hábito</option>
        {availableHabits.map((habit) => (
          <option key={habit.id} value={habit.id}>
            {habit.nome}
          </option>
        ))}
      </select>

      {/* Descrição */}
      <textarea
        value={descricao}
        onChange={(e) => setDescricao(e.target.value)}
        placeholder="Descrição do hábito (até 255 caracteres)"
        maxLength={255}
        className="p-2 border border-gray-300 rounded-lg resize-none"
        required
      />

      {/* Frequência */}
      <div className="flex flex-col gap-2">
        <label className="font-medium">Frequência:</label>
        <div className="flex gap-4">
          {Object.values(Frequencia).map((freq) => (
            <label key={freq} className="flex items-center gap-1">
              <input
                type="radio"
                checked={frequencia === freq}
                onChange={() => setFrequencia(freq)}
                className="h-4 w-4 text-indigo-600"
              />
              <span>{freq.charAt(0).toUpperCase() + freq.slice(1)}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Data de início */}
      <div className="flex flex-col gap-1">
        <label htmlFor="dataInicio" className="font-medium">
          Data de início:
        </label>
        <input
          type="date"
          id="dataInicio"
          value={dataInicio}
          onChange={(e) => setDataInicio(e.target.value)}
          className="p-2 border border-gray-300 rounded-lg"
          required
        />
      </div>

      {/* Vezes na semana (condicional) */}
      {frequencia === Frequencia.SEMANAL && (
        <div className="flex flex-col gap-1">
          <label htmlFor="vezesNaSemana" className="font-medium">
            Vezes por semana:
          </label>
          <input
            type="number"
            id="vezesNaSemana"
            min="1"
            max="7"
            value={vezesNaSemana ?? ""}
            onChange={(e) => setVezesNaSemana(Number(e.target.value))}
            className="p-2 border border-gray-300 rounded-lg"
            required
          />
        </div>
      )}

      {/* Botão de submit */}
      <button
        type="submit"
        disabled={loadingHabit}
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
      >
        {loadingHabit ? "Adicionando..." : "Adicionar Hábito"}
      </button>

      {/* Mensagens de feedback */}
      {mensagem && <p className="text-green-600">{mensagem}</p>}
      {(erro || errorHabit) && (
        <p className="text-red-600">{erro || errorHabit}</p>
      )}
    </form>
  );
}