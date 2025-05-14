'use client';

import { useState } from 'react';
import PieChart from '@/app/components/pie_chart';
import BarChart from '@/app/components/bar_chart';
import ProgressChart from '@/app/components/progress_chart';

export default function DashboardPage() {
  // Dados ajustados para corresponder às interfaces esperadas
  const [chartData] = useState({
    // Dados para o PieChart (precisa de value e color)
    categories: [
      { name: 'Saúde', value: 35, color: '#8B5CF6' },
      { name: 'Produtividade', value: 25, color: '#7C3AED' },
      { name: 'Bem-estar', value: 20, color: '#6D28D9' },
      { name: 'Aprendizado', value: 15, color: '#5B21B6' },
      { name: 'Outros', value: 5, color: '#4C1D95' }
    ],
    
    // Dados para o BarChart (precisa de completion)
    habits: [
      { name: 'Beber água', completion: 80 },
      { name: 'Exercícios', completion: 65 },
      { name: 'Leitura', completion: 45 },
      { name: 'Meditação', completion: 30 }
    ],
    
    // Dados para o ProgressChart
    weeklyProgress: [
      { day: 'Seg', completed: 4, total: 5 },
      { day: 'Ter', completed: 3, total: 5 },
      { day: 'Qua', completed: 5, total: 5 },
      { day: 'Qui', completed: 2, total: 5 },
      { day: 'Sex', completed: 4, total: 5 },
      { day: 'Sáb', completed: 1, total: 3 },
      { day: 'Dom', completed: 0, total: 2 }
    ]
  });

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
            <PieChart data={chartData.categories} />
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