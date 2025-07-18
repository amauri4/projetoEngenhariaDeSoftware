"use client";

import { useAuth } from "@/app/hooks/use_auth";
import { useTarefas } from "@/app/hooks/use_tarefas";
import { useFuncionarios } from "@/app/hooks/use_funcionarios";

import TarefaForm from "@/app/components/tarefa_form";
import GerenteTarefaList from "@/app/components/gerente_tarefa_list";
import FuncionarioTarefaList from "@/app/components/funcionario_tarefa_list";

export default function TarefasDashboardPage() {
  const { id: atorId, nome: atorNome, tipo: atorTipo } = useAuth();
  const { tarefas, loading, error, refetch } = useTarefas(atorId);
  const { funcionarios, loading: loadingFuncionarios } = useFuncionarios(atorId);

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
