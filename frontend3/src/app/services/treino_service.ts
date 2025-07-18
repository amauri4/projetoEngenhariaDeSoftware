import { Treino, TreinoCreateInput } from "@/app/types/treino";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getTreinosPorAtorService(atorId: number): Promise<Treino[]> {
  const response = await fetch(`${API_URL}/treinos/ator/${atorId}`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar treinos.");
  }
  return response.json();
}

export async function addTreinoService(instrutorId: number, data: TreinoCreateInput): Promise<Treino> {
  const response = await fetch(`${API_URL}/treinos/instrutor/${instrutorId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao adicionar treino.");
  }
  const result = await response.json();
  return result.treino;
}

export async function updateTreinoService(treinoId: number, data: Partial<TreinoCreateInput>): Promise<Treino> {
    const response = await fetch(`${API_URL}/treinos/${treinoId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.erro || "Erro ao atualizar treino.");
    }
    const result = await response.json();
    return result.treino;
}

export async function deleteTreinoService(treinoId: number): Promise<boolean> {
  const response = await fetch(`${API_URL}/treinos/${treinoId}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao remover treino.");
  }
  return response.status === 204;
}