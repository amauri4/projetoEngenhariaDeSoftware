"use client";

import type { HabitoUsuario } from "@/app/types/habito_usuario";
import { useHabits } from "@/app/hooks/use_lista_habitos";
import useDeleteHabit from "@/app/hooks/use_remove_habitos";
import { useEffect, useState } from "react";
import { HabitDetailsModal } from "@/app/components/habit_details";
import { format, isSameDay } from "date-fns";
import { Frequencia } from "@/app/types/frequencia";
import { RegistroDiario, RegistroDiarioUpdateInput } from "@/app/types/registro_habito";
import { useRegistroDiario } from "@/app/hooks/use_registro_diario";

// TODO: -> RESOLVER ERRO NA EXIBIÇÃO DOS HÁBITOS

export interface HabitListProps {
  habits: HabitoUsuario[];
  onRemove: (idRemovido: number) => void;
  selectedDate: Date;
}

export default function HabitList({ habits, onRemove, selectedDate }: HabitListProps) {
  const { habits: availableHabits } = useHabits();
  const { deleteHabit, loadingDeleteHabit } = useDeleteHabit();
  const [selectedHabit, setSelectedHabit] = useState<HabitoUsuario | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [firstLoad, setFirstLoad] = useState(true);
  const { createRegistro, getRegistrosPorDataEspecifica, updateRegistro, loading, error } = useRegistroDiario();
 
  const habitNamesMap = new Map<number, string>();
  availableHabits?.forEach((habit) => {
    habitNamesMap.set(habit.id, habit.nome);
  });

  const handleRemove = async (habit: HabitoUsuario) => {
    if (!habit.id) {
      console.error("Hábito sem ID, impossível remover.");
      return;
    }

    const sucesso = await deleteHabit(habit.id);
    if (sucesso) {
      onRemove(habit.id);
    } else {
      console.error("Erro ao remover hábito.");
    }
  };

  const openHabitDetails = (habit: HabitoUsuario) => {
    setSelectedHabit(habit);
    setIsModalOpen(true);
  };

  const filteredHabits = habits.filter(habit => {
    const habitStartDate = new Date(habit.data_inicio);

    if (habitStartDate > selectedDate) return false;

    switch (habit.frequencia) {
      case Frequencia.DIARIA:
        
        const diasSemanaNumeros = (habit.dias_semana as unknown as string[]).map(dia => {
          if (!isNaN(Number(dia))) {
            return Number(dia);
          }
          
          // Se for texto, converte de acordo com os dias da semana
          const diaLower = dia.toString().toLowerCase().trim();
          const mapeamento: Record<string, number> = {
            'domingo': 0,
            'segunda': 1,
            'terca': 2,
            'quarta': 3,
            'quinta': 4,
            'sexta': 5,
            'sabado': 6
          };
          
          return mapeamento[diaLower] ?? 0;
        });
        
        return diasSemanaNumeros.includes(selectedDate.getDay());
      case Frequencia.SEMANAL:
        return true;
      case Frequencia.MENSAL:
        return habit.dias_mes?.includes(selectedDate.getDate()) ?? false;
      default:
        return false;
    }
  });

  useEffect(() => {
    setFirstLoad(false);
  }, [])

  useEffect(() => {
  
    const verificarECriarRegistros = async () => {
      try {
        const dataFormatada = selectedDate.toISOString().split('T')[0];
        const usuarioId = Number(localStorage.getItem('usuario_id'));
        
        const registrosDoDia = await getRegistrosPorDataEspecifica(usuarioId, dataFormatada);
  
        for (const habit of filteredHabits) {
          const existeRegistro = registrosDoDia.some(r => r.habito_id === habit.id);
          if (!existeRegistro) {
            await createRegistro({
              data: dataFormatada,
              habito_id: habit.id,
              concluido: false
            });
          }
        }
      } catch (error) {
        console.error("Erro ao verificar/criar registros:", error);
      }
    };
  
    verificarECriarRegistros();
  }, [selectedDate, firstLoad]);

  const handleToggleComplete = async (registroId: number, registroData: RegistroDiarioUpdateInput) => {
    try {
      await updateRegistro(registroId, registroData);
    } catch (error) {
      console.error("Erro ao atualizar registro:", error);
      throw error;
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">
        Seus hábitos para {format(selectedDate, "dd/MM/yyyy")}
      </h2>
      
      {filteredHabits.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhum hábito para esta data.</p>
      ) : (
        <ul className="space-y-2">
          {filteredHabits.map((habit) => (
            <li
              key={habit.id}
              className="flex justify-between items-center bg-gray-100 p-3 rounded-lg hover:bg-gray-200 transition-colors cursor-pointer"
              onClick={() => openHabitDetails(habit)}
            >
              <div className="flex-1">
                <h3 className="font-medium">
                  {habitNamesMap.get(habit.habito_base_id) ?? "Hábito desconhecido"}
                </h3>
                {habit.descricao && (
                  <p className="text-sm text-gray-600 truncate">{habit.descricao}</p>
                )}
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemove(habit);
                }}
                disabled={loadingDeleteHabit}
                className="ml-4 text-red-500 hover:text-red-700 text-sm disabled:opacity-50"
              >
                {loadingDeleteHabit ? "Removendo..." : "Remover"}
              </button>
            </li>
          ))}
        </ul>
      )}

      <HabitDetailsModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        habit={selectedHabit}
        selectedDate={selectedDate}
        onToggleComplete={handleToggleComplete}
        getRegistrosPorDataEspecifica={getRegistrosPorDataEspecifica}
      />
    </div>
  );
}
