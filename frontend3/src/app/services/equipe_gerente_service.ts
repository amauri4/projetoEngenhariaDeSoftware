import { Funcionario } from "@/app/types/funcionario";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getEquipeByGerenteService(gerenteId: number): Promise<Funcionario[]> {
  const response = await fetch(`${API_URL}/auth3/${gerenteId}/equipe`);

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar a equipe.");
  }

  return response.json();
}
