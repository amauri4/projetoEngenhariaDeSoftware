"use client";

import { useAuth } from "@/app/hooks/use_auth";
import { useTreinos } from "@/app/hooks/use_treinos";
import { useAlunos } from "@/app/hooks/use_alunos"; 
import TreinoForm from "@/app/components/treino_form";
import InstrutorTreinoList from "@/app/components/instrutor_treino_list";
import AlunoTreinoList from "@/app/components/aluno_treino_list";

export default function TreinosDashboardPage() {
  const { id: atorId, nome: atorNome, tipo: atorTipo } = useAuth();
  const { treinos, loading, error, adicionarTreinoLocalmente } = useTreinos(atorId);
  const { alunos, loading: loadingAlunos } = useAlunos(atorId); 

  const renderContent = () => {
    if (!atorId || !atorTipo) {
      return <p className="text-center">Carregando dados do usuário...</p>;
    }
    
    if (loading) {
      return <p className="text-center">Carregando treinos...</p>;
    }

    if (error) {
      return <p className="text-red-500 text-center">Erro: {error}</p>;
    }

    if (atorTipo === 'instrutor') {
      return (
        <>
          <section className="mb-8 mt-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Criar Novo Treino</h2>
            <TreinoForm 
              instrutorId={atorId}
              alunos={alunos} 
              onAdd={adicionarTreinoLocalmente}
            />
          </section>
          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Treinos Atuais dos Alunos</h2>
            <InstrutorTreinoList treinos={treinos} />
          </section>
        </>
      );
    }

    if (atorTipo === 'aluno') {
      return (
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Meus Treinos</h2>
          <AlunoTreinoList treinos={treinos} atorId={atorId} />
        </section>
      );
    }
    
    return null;
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start bg-gradient-to-br from-yellow-400 to-orange-500 p-6">
      <main className="w-full max-w-4xl bg-white rounded-2xl shadow-xl p-8 sm:p-10">
        <h1 className="text-3xl font-bold text-center text-orange-700 mb-4">
          Painel de Treinos
        </h1>
        <p className="text-center text-gray-600 mb-6">Bem-vindo(a), {atorNome || 'Usuário'}!</p>
        
        {renderContent()}
      </main>
    </div>
  );
}
