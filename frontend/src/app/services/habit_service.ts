import { HabitoUsuario } from "@/app/types/habito_usuario";

export async function fetchHabitosUsuario(email: string): Promise<HabitoUsuario[]> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/habitos-usuario/${email}/habitos`);

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.erro || "Erro ao buscar hábitos do usuário.");
  }

  const data: HabitoUsuario[] = await response.json();
  return data;
}
