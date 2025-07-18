import { HabitoBase } from "@/app/types/habito_base";

const listaHabitosRoute = `${process.env.NEXT_PUBLIC_API_URL}/habitos`;

export async function fetchHabitosBase(): Promise<HabitoBase[]> {
  const response = await fetch(listaHabitosRoute);

  if (!response.ok) {
    throw new Error("Falha ao carregar hábitos");
  }

  const data: HabitoBase[] = await response.json();
  return data;
}
