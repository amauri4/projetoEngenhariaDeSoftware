import { useCallback } from "react";
import type { Habito } from "@/app/types/habit";

export function useRemoveHabit(onSuccess?: (index: number) => void) {
  const removeHabit = useCallback(
    async (habit: Habito, index: number) => {
      // Aqui você pode fazer uma chamada à API se quiser persistência, por exemplo:
      // await fetch(`/api/remover-habito/${habit.id}`, { method: "DELETE" });

      if (onSuccess) {
        onSuccess(index);
      }
    },
    [onSuccess]
  );

  return { removeHabit };
}
