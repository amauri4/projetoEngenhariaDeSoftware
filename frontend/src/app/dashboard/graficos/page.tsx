'use client';

import { useEffect, useState } from 'react';
import PieChart from '@/app/components/pie_chart';
import BarChart from '@/app/components/bar_chart';
import ProgressChart from '@/app/components/progress_chart';
import { buscarCategoriasDoUsuario } from '@/app/services/habit_service';
import { useCorrelacoes } from '@/app/hooks/use_correlacao_habitos';

const CATEGORY_COLORS = [
  '#8B5CF6', '#7C3AED', '#6D28D9', '#5B21B6', '#4C1D95',
  '#3B82F6', '#2563EB', '#1D4ED8', '#1E40AF', '#1E3A8A'
];

interface CategoryData {
  name: string;
  value: number;
  color: string;
}

interface HabitData {
  name: string;
  completion: number;
}

interface WeeklyProgressData {
  day: string;
  completed: number;
  total: number;
}

interface ChartData {
  categories: CategoryData[];
  habits: HabitData[];
  weeklyProgress: WeeklyProgressData[];
}

export default function DashboardPage() {
  const [chartData, setChartData] = useState<ChartData>({
    categories: [],
    habits: [],
    weeklyProgress: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAnalysis, setShowAnalysis] = useState(false);

  const {
    correlacoes,
    loading: loadingCorrelacoes,
    error: errorCorrelacoes,
    buscarCorrelacoes
  } = useCorrelacoes();

  useEffect(() => {
    async function loadData() {
      try {
        // Buscar categorias da API
        const id = 1;
        const categoriasApi = await buscarCategoriasDoUsuario(id);

        const categoriesData = Object.entries(categoriasApi).map(([name, value], index) => ({
          name,
          value,
          color: CATEGORY_COLORS[index % CATEGORY_COLORS.length]
        }));

        // Dados mockados para os outros gráficos 
        const habitsData = [
          { name: 'Beber água', completion: 80 },
          { name: 'Exercícios', completion: 65 },
          { name: 'Leitura', completion: 45 },
          { name: 'Meditação', completion: 30 }
        ];

        const weeklyProgressData = [
          { day: 'Seg', completed: 4, total: 5 },
          { day: 'Ter', completed: 3, total: 5 },
          { day: 'Qua', completed: 5, total: 5 },
          { day: 'Qui', completed: 2, total: 5 },
          { day: 'Sex', completed: 4, total: 5 },
          { day: 'Sáb', completed: 1, total: 3 },
          { day: 'Dom', completed: 0, total: 2 }
        ];

        setChartData({
          categories: categoriesData,
          habits: habitsData,
          weeklyProgress: weeklyProgressData
        });

        await buscarCorrelacoes(id);

      } catch (err) {
        if (err instanceof Error) {
          setError(null);
        }
        console.error("Erro ao carregar dados:", err);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100 p-6">

      <header className="mb-8 md:mb-10 flex flex-col items-center text-center space-y-2">
        <h1 className="text-3xl md:text-3xl font-bold text-purple-900">Meu Progresso</h1>
        <p className="text-md md:text-base text-purple-700">Visualize seu desempenho e conquistas</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gráfico de Pizza - Categorias */}
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h2 className="text-xl font-semibold text-purple-800 mb-4">Distribuição por Categoria</h2>
          <div className="h-64">
            <PieChart data={chartData.categories ? chartData.categories : []} />
          </div>
        </div>

        {/* Gráfico de Barras - Hábitos concluídos */}
        <div className="bg-white rounded-xl p-6 shadow-md">
          <h2 className="text-xl font-semibold text-purple-800 mb-4">Taxa de Conclusão</h2>
          <div className="h-64">
            <BarChart data={chartData.habits} />
          </div>
        </div>
      </div>

      {/* Progresso Semanal */}
      <div className="bg-white rounded-xl p-6 shadow-md mb-8">
        <h2 className="text-xl font-semibold text-purple-800 mb-4">Progresso Semanal</h2>
        <ProgressChart data={chartData.weeklyProgress} />
      </div>

      {/* Área para Interações com LLM - ATUALIZADA */}
      <div className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-xl font-semibold text-purple-800 mb-4">Análise Personalizada</h2>
        <div className="min-h-40 p-4 border-2 border-dashed border-purple-200 rounded-lg bg-purple-50">
          {!showAnalysis ? (
            <button
              onClick={() => setShowAnalysis(true)}
              className="w-full h-full flex flex-col items-center justify-center space-y-2"
            >
              <svg className="w-10 h-10 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <p className="text-purple-600 font-medium">Gerar análise de correlações entre hábitos</p>
            </button>
          ) : (
            <div className="space-y-4">
              <h3 className="font-semibold text-purple-700">Correlações entre seus hábitos:</h3>

              {loadingCorrelacoes && (
                <div className="flex justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-500"></div>
                </div>
              )}

              {errorCorrelacoes && (
                <p className="text-red-500 text-center">{errorCorrelacoes}</p>
              )}

              {correlacoes && !loadingCorrelacoes && (
                <div className="bg-purple-100 p-3 rounded-md">
                  <ul className="list-disc pl-5 space-y-1 text-purple-800">
                    {correlacoes.split('\n').map((item, index) => (
                      item.trim() && <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={() => setShowAnalysis(false)}
                className="mt-2 text-sm text-purple-600 hover:text-purple-800"
              >
                Ocultar análise
              </button>
            </div>
          )}
        </div>
      </div>

    </div>
  );
}