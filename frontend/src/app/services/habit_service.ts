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

export async function buscarCategoriasDoUsuario(usuario_id: number): Promise<Record<string, number>> {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/habitos-usuario/${usuario_id}/categorias-usuario`
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.erro || "Erro ao buscar categorias de hábito do usuário");
    }

    const categorias: Record<string, number> = await response.json();
    return categorias;

  } catch (error) {
    console.error("Erro na requisição de categorias:", error);
    throw new Error(
      error instanceof Error 
        ? error.message 
        : "Erro desconhecido ao buscar categorias de hábito"
    );
  }
}