"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { TreinoSchema, TreinoCreateInput } from "@/app/schemas/TreinoSchema";
import { Treino } from "@/app/types/treino";
import { Aluno } from "@/app/types/aluno";
import { addTreinoService } from "@/app/services/treino_service";
import { format } from "date-fns";
import { createOcorrenciaTreinoService } from "@/app/services/ocorrencia_treino_service"; 
import { OcorrenciaCreateInput } from "../types/ocorrencia";

interface TreinoFormProps {
  instrutorId: number | null;
  alunos: Aluno[];
  onAdd: (novoTreino: Treino) => void;
}

export default function TreinoForm({ instrutorId, alunos, onAdd }: TreinoFormProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<TreinoCreateInput>({
    resolver: zodResolver(TreinoSchema),
    defaultValues: {
      data_inicio: format(new Date(), "yyyy-MM-dd"),
    },
  });

  const onSubmit = async (data: TreinoCreateInput) => {
    if (!instrutorId) {
      setError("ID do instrutor não encontrado. Faça o login.");
      return;
    }
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const novoTreino = await addTreinoService(instrutorId, data);
      
      if (novoTreino && novoTreino.id && data.data_entrega) {
        const ocorrenciaInput: OcorrenciaCreateInput = {
          treino_id: novoTreino.id,
          data: data.data_entrega,
          status: false
        };
        await createOcorrenciaTreinoService(ocorrenciaInput);
      }

      setSuccessMessage("Treino adicionado com sucesso!");
      reset();
      onAdd(novoTreino); 
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao adicionar treino.");
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
        <label className="font-medium">Descrição do Treino:</label>
        <textarea
          {...register("descricao")}
          placeholder="Descreva o treino a ser realizado"
          className="p-2 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-orange-500"
        />
        {errors.descricao && <p className="text-red-500 text-sm">{errors.descricao.message}</p>}
      </div>

      {/* Responsável (Aluno) */}
      <div className="flex flex-col gap-1">
        <label className="font-medium">Atribuir para:</label>
        <select
          {...register("id_aluno_responsavel", { valueAsNumber: true })}
          className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500"
        >
          <option value="">Selecione um aluno</option>
          {alunos.map((aluno) => (
            <option key={aluno.id} value={aluno.id}>
              {aluno.nome}
            </option>
          ))}
        </select>
        {errors.id_aluno_responsavel && <p className="text-red-500 text-sm">{errors.id_aluno_responsavel.message}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Data de Início */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">Data de Início:</label>
          <input
            type="date"
            {...register("data_inicio")}
            className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500"
          />
          {errors.data_inicio && <p className="text-red-500 text-sm">{errors.data_inicio.message}</p>}
        </div>

        {/* Data de Entrega (Prazo) */}
        <div className="flex flex-col gap-1">
          <label className="font-medium">Data de Entrega:</label>
          <input
            type="date"
            {...register("data_entrega")}
            className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500"
          />
          {errors.data_entrega && <p className="text-red-500 text-sm">{errors.data_entrega.message}</p>}
        </div>
      </div>

      {/* Botão de submit */}
      <button
        type="submit"
        disabled={loading}
        className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 disabled:opacity-50 mt-4"
      >
        {loading ? "Adicionando..." : "Adicionar Treino"}
      </button>
      
      {successMessage && <div className="p-3 bg-green-100 text-green-800 rounded-lg">{successMessage}</div>}
      {error && <div className="p-3 bg-red-100 text-red-800 rounded-lg">{error}</div>}
    </form>
  );
}
