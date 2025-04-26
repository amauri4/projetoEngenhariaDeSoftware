import { HabitoUsuario } from "@/app/types/habito_usuario";

export async function addHabitService(
  usuarioId: number,
  habitoBaseId: number,
  descricao: string
): Promise<HabitoUsuario> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/habitos-usuario/${usuarioId}/habitos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ descricao, habito_base_id: habitoBaseId }),
  });

  if (!response.ok) {
    throw new Error("Erro ao adicionar hábito");
  }

  const data = await response.json();
  console.log(data.habito_usuario)
  return data.habito_usuario;
}
