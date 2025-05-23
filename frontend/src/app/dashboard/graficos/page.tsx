'use client';

import { useEffect, useState } from 'react';
import PieChart from '@/app/components/pie_chart';
import BarChart from '@/app/components/bar_chart';
import ProgressChart from '@/app/components/progress_chart';
import { buscarCategoriasDoUsuario } from '@/app/services/habit_service';

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

      } catch (err) {
        if (err instanceof Error){
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

      {/* Área para Interações com LLM */}
      <div className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-xl font-semibold text-purple-800 mb-4">Análise Personalizada</h2>
        <div className="min-h-40 p-4 border-2 border-dashed border-purple-200 rounded-lg bg-purple-50">
          <p className="text-purple-600 text-center">
            Área para integração com modelos de IA e análises personalizadas
          </p>
        </div>
      </div>

    </div>
  );
}