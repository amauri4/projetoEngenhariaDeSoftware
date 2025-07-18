"use client";

import { useAuth } from "@/app/hooks/use_auth";
import { useTarefas } from "@/app/hooks/use_tarefas";
import { useFuncionarios } from "@/app/hooks/use_funcionarios";
import { getProdutividadeEquipeInsight } from "@/app/services/insight_service";
import { useState } from "react";
import TarefaForm from "@/app/components/tarefa_form";
import GerenteTarefaList from "@/app/components/gerente_tarefa_list";
import FuncionarioTarefaList from "@/app/components/funcionario_tarefa_list";

export default function TarefasDashboardPage() {
  const { id: atorId, nome: atorNome, tipo: atorTipo } = useAuth();
  const { tarefas, loading, error, refetch } = useTarefas(atorId);
  const { funcionarios, loading: loadingFuncionarios } = useFuncionarios(atorId);
  const [insight, setInsight] = useState<string | null>(null);
  const [loadingInsight, setLoadingInsight] = useState(false);
  const [errorInsight, setErrorInsight] = useState<string | null>(null);
  const [showInsight, setShowInsight] = useState(false);

  const handleGerarInsight = async () => {
    if (!atorId) return;
    setShowInsight(true);
    setLoadingInsight(true);
    setErrorInsight(null);
    setInsight(null);
    try {
      const resultado = await getProdutividadeEquipeInsight(atorId);
      setInsight(resultado);
    } catch (err) {
      setErrorInsight(err instanceof Error ? err.message : "Erro desconhecido.");
    } finally {
      setLoadingInsight(false);
    }
  };

  const renderContent = () => {
    if (!atorId || !atorTipo) {
      return <p>Carregando dados do usuário...</p>;
    }

    if (loading) {
      return <p>Carregando tarefas...</p>;
    }

    if (error) {
      return <p className="text-red-500">Erro: {error}</p>;
    }

    // --- VISÃO DO GERENTE ---
    if (atorTipo === 'gerente') {
      return (
        <>
          <section className="mb-8 mt-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Criar Nova Tarefa</h2>
            <TarefaForm
              gerenteId={atorId}
              funcionarios={funcionarios}
              onAdd={refetch}
            />
          </section>
          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Tarefas da Equipe</h2>
            <GerenteTarefaList tarefas={tarefas} />
          </section>

          <section className="mb-8 mt-6 p-6 border rounded-lg bg-gray-50">
            {!showInsight ? (
              <button
                onClick={handleGerarInsight}
                className="bg-white-500 text-blue-700 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors w-full"
              >
                Gerar Insight de Produtividade da Equipe
              </button>
            ) : (
              <div className="space-y-4">
                <h3 className="font-semibold text-blue-700">Análise de Produtividade da Equipe:</h3>

                {loadingInsight && (
                  <div className="flex justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                  </div>
                )}

                {errorInsight && (
                  <p className="text-red-500 text-center">{errorInsight}</p>
                )}

                {insight && !loadingInsight && (
                  <div className="bg-blue-100 p-3 rounded-md">
                    <ul className="list-disc pl-5 space-y-1 text-blue-800">
                      {insight.split('\n').map((item, index) => (
                        item.trim() && <li key={index}>{item.replace('-', '').trim()}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  onClick={() => setShowInsight(false)}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-800"
                >
                  Ocultar análise
                </button>
              </div>
            )}
          </section>

        </>
      );
    }

    // --- VISÃO DO FUNCIONÁRIO ---
    if (atorTipo === 'funcionario') {
      return (
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Minhas Tarefas</h2>
          <FuncionarioTarefaList tarefas={tarefas} atorId={atorId} />
        </section>
      );
    }

    return null;
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-blue-500 to-teal-500 p-6">
      <main className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-blue-700 mb-4">
          Painel de Tarefas
        </h1>
        <p className="text-center text-gray-600 mb-6">Bem-vindo(a), {atorNome || 'Usuário'}!</p>

        {renderContent()}
      </main>
    </div>
  );
}
