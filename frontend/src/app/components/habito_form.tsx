"use client";

import { useEffect, useState } from "react";
import type { HabitoBase } from "@/app/types/habito_base";
import useAddHabit from "@/app/hooks/use_add_habitos";
import { Frequencia } from "@/app/types/frequencia";
import { format } from "date-fns";

export interface HabitFormProps {
  availableHabits: HabitoBase[];
  onAdd: () => void;
  idUsuario: number | null;
}

const DIAS_SEMANA = [
  { id: 1, nome: "Segunda" },
  { id: 2, nome: "Terça" },
  { id: 3, nome: "Quarta" },
  { id: 4, nome: "Quinta" },
  { id: 5, nome: "Sexta" },
  { id: 6, nome: "Sábado" },
  { id: 7, nome: "Domingo" },
];

const DIAS_MES = Array.from({ length: 31 }, (_, i) => i + 1);

export default function HabitForm({ onAdd, availableHabits, idUsuario }: HabitFormProps) {
  const [selectedHabitId, setSelectedHabitId] = useState<number | null>(null);
  const [descricao, setDescricao] = useState("");
  const [frequencia, setFrequencia] = useState<Frequencia>(Frequencia.DIARIA);
  const [dataInicio, setDataInicio] = useState<string>(format(new Date(), "yyyy-MM-dd"));
  const [vezesNaSemana, setVezesNaSemana] = useState<number | null>(null);
  const [diasSelecionados, setDiasSelecionados] = useState<number[]>([]);
  const [diasMesSelecionados, setDiasMesSelecionados] = useState<number[]>([]);
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

    if (frequencia === Frequencia.DIARIA && diasSelecionados.length === 0) {
      setErro("Selecione pelo menos um dia da semana.");
      return;
    }

    if (frequencia === Frequencia.MENSAL && diasMesSelecionados.length === 0) {
      setErro("Selecione pelo menos um dia do mês.");
      return;
    }

    try {
      await addHabit(
        selectedHabitId,
        descricao,
        frequencia,
        dataInicio,
        vezesNaSemana ? vezesNaSemana : null,
        diasSelecionados ? diasSelecionados : [],
        diasMesSelecionados ? diasMesSelecionados : []
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
    setDataInicio(format(new Date(), "yyyy-MM-dd"));
    setVezesNaSemana(null);
    setDiasSelecionados([]);
    setErro(null);
  };

  const toggleDiaSelecionado = (dia: number) => {
    setDiasSelecionados(prev =>
      prev.includes(dia)
        ? prev.filter(d => d !== dia)
        : [...prev, dia]
    );
  };

  const toggleDiaMesSelecionado = (dia: number) => {
    setDiasMesSelecionados(prev =>
      prev.includes(dia) 
        ? prev.filter(d => d !== dia) 
        : [...prev, dia]
    );
  };

  useEffect(() => {
    if (mensagem) {
      const timer = setTimeout(() => setMensagem(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [mensagem]);

  useEffect(() => {
    setDiasSelecionados([]);
    if (frequencia !== Frequencia.SEMANAL) {
      setVezesNaSemana(null);
    }
  }, [frequencia]);

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
      {/* Seleção de hábito */}
      <div className="flex flex-col gap-1">
        <label className="font-medium">Hábito:</label>
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
      </div>

      {/* Descrição */}
      <div className="flex flex-col gap-1">
        <label className="font-medium">Descrição:</label>
        <textarea
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
          placeholder="Descreva seu hábito (até 255 caracteres)"
          maxLength={255}
          className="p-2 border border-gray-300 rounded-lg resize-none"
          required
        />
      </div>

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

      {/* Data de início - Corrigido para usar o formato correto */}
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
          min={format(new Date(), "yyyy-MM-dd")}
          required
        />
      </div>

      {/* Condicional para cada tipo de frequência */}
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

      {frequencia === Frequencia.DIARIA && (
        <div className="flex flex-col gap-2">
          <label className="font-medium">Dias da semana:</label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {DIAS_SEMANA.map((dia) => (
              <label key={dia.id} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={diasSelecionados.includes(dia.id)}
                  onChange={() => toggleDiaSelecionado(dia.id)}
                  className="h-4 w-4 text-indigo-600"
                />
                <span>{dia.nome}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {frequencia === Frequencia.MENSAL && (
        <div className="flex flex-col gap-2">
          <label className="font-medium">Dias do mês:</label>
          <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
            {DIAS_MES.map((dia) => (
              <label key={dia} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={diasMesSelecionados.includes(dia)}
                  onChange={() => toggleDiaMesSelecionado(dia)}
                  className="h-4 w-4 text-indigo-600"
                />
                <span>{dia}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {/* Botão de submit */}
      <button
        type="submit"
        disabled={loadingHabit}
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 mt-4"
      >
        {loadingHabit ? "Adicionando..." : "Adicionar Hábito"}
      </button>

      {/* Mensagens de feedback */}
      {mensagem && (
        <div className="p-3 bg-green-100 text-green-800 rounded-lg">
          {mensagem}
        </div>
      )}
      {(erro || errorHabit) && (
        <div className="p-3 bg-red-100 text-red-800 rounded-lg">
          {erro || errorHabit}
        </div>
      )}
    </form>
  );
}