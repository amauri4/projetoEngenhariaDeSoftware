import { useHabits } from "@/app/hooks/use_lista_habitos";

const useHabitNameById = (habitoId: number | null | undefined): string | null => {
  const { habits } = useHabits();

  if (!habitoId || !habits || habits.length === 0) return null;

  const habito = habits.find((h) => h.id === habitoId);
  return habito ? habito.nome : null;
};

export default useHabitNameById;
