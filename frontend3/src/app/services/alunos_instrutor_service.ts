import { Aluno } from "@/app/types/aluno";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getAlunosByInstrutor(instrutor_id: number): Promise<Aluno[]> {
  const response = await fetch(`${API_URL}/auth3/${instrutor_id}/alunos`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar os alunos.");
  }

  return response.json();
}
