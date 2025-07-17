"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { TarefaSchema, TarefaCreateInput } from "@/app/schemas/TarefaSchema";
import { addTarefaService } from "@/app/services/tarefa_service";
import { format } from "date-fns";
import { createOcorrenciaService } from "@/app/services/ocorrencia_tarefa_service";

interface Funcionario {
  id: number;
  nome: string;
}

export interface TarefaFormProps {
  gerenteId: number | null;
  funcionarios: Funcionario[];
  onAdd: () => void;
}

export default function TarefaForm({ gerenteId, funcionarios, onAdd }: TarefaFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TarefaCreateInput>({
    resolver: zodResolver(TarefaSchema),
    defaultValues: {
      dataInicio: format(new Date(), "yyyy-MM-dd"),
    },
  });

  const onSubmit = async (data: TarefaCreateInput) => {
    if (!gerenteId) {
      setError("ID do gerente não encontrado. Faça o login.");
      return;
    }
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const novaTarefa = await addTarefaService(gerenteId, data);

      if (novaTarefa && novaTarefa.id && data.prazoFinal) {
        await createOcorrenciaService(novaTarefa.id, data.prazoFinal, false);
      }

      setSuccessMessage("Tarefa adicionada com sucesso!");
      reset();
      onAdd(); 
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao adicionar tarefa.");
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 mt-4">
      {/* Descrição */}
      <div className="flex flex-col gap-1">
        <label className="font-medium">Descrição da Tarefa:</label>
        <textarea
          {...register("descricao")}
          placeholder="Descreva a tarefa a ser realizada"
          className="p-2 border border-gray-300 rounded-lg resize-none"
        />
        {errors.descricao && <p className="text-red-500 text-sm">{errors.descricao.message}</p>}
      </div>

      {/* Responsável */}
      <div className="flex flex-col gap-1">
        <label className="font-medium">Atribuir para:</label>
        <select
          {...register("responsavelId", { valueAsNumber: true })}
          className="p-2 border border-gray-300 rounded-lg"
        >
          <option value="">Selecione um funcionário</option>
          {funcionarios.map((func) => (
            <option key={func.id} value={func.id}>
              {func.nome}
            </option>
          ))}
        </select>
        {errors.responsavelId && <p className="text-red-500 text-sm">{errors.responsavelId.message}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Data de Início */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">Data de Início:</label>
          <input
            type="date"
            {...register("dataInicio")}
            className="p-2 border border-gray-300 rounded-lg"
          />
          {errors.dataInicio && <p className="text-red-500 text-sm">{errors.dataInicio.message}</p>}
        </div>

        {/* Prazo Final */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">Prazo Final:</label>
          <input
            type="date"
            {...register("prazoFinal")}
            className="p-2 border border-gray-300 rounded-lg"
          />
          {errors.prazoFinal && <p className="text-red-500 text-sm">{errors.prazoFinal.message}</p>}
        </div>
      </div>

      {/* Botão de submit */}
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 mt-4"
      >
        {loading ? "Adicionando..." : "Adicionar Tarefa"}
      </button>
      
      {/* Mensagens de feedback */}
      {successMessage && <div className="p-3 bg-green-100 text-green-800 rounded-lg">{successMessage}</div>}
      {error && <div className="p-3 bg-red-100 text-red-800 rounded-lg">{error}</div>}
    </form>
  );
}
