import { Ocorrencia, OcorrenciaCreateInput } from "@/app/types/ocorrencia";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getOcorrenciasPorAtorService(atorId: number): Promise<Ocorrencia[]> {
  const response = await fetch(`${API_URL}/ocorrencias-treino/ator/${atorId}`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar ocorrências.");
  }
  return response.json();
}

export async function getOcorrenciasConcluidasPorAtorService(atorId: number): Promise<Ocorrencia[]> {
    const response = await fetch(`${API_URL}/ocorrencias-treino/ator/${atorId}/concluidas`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.erro || "Erro ao buscar ocorrências concluídas.");
    }
    return response.json();
}

export async function createOcorrenciaTreinoService(data: OcorrenciaCreateInput): Promise<Ocorrencia> {
    const response = await fetch(`${API_URL}/ocorrencias-treino/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.erro || "Erro ao criar ocorrência.");
    }
    const result = await response.json();
    return result.ocorrencia;
}

export async function getOcorrenciasTreinoPorDataService(atorId: number, dataInicio?: string, dataFim?: string): Promise<Ocorrencia[]> {
  const params = new URLSearchParams();
  if (dataInicio) params.append('data_inicio', dataInicio);
  if (dataFim) params.append('data_fim', dataFim);

  const response = await fetch(`${API_URL}/ocorrencias-treino/ator/${atorId}/data?${params.toString()}`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar ocorrências de treino por data.");
  }
  return response.json();
}

export async function getOcorrenciasPorDataEspecificaService(atorId: number, data: string): Promise<Ocorrencia[]> {
    const response = await fetch(`${API_URL}/ocorrencias-treino/ator/${atorId}/data_especifica?data=${data}`);
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.erro || "Erro ao buscar ocorrências em data específica.");
    }
    return response.json();
}

export async function updateOcorrenciaTreinoStatusService(ocorrenciaId: number, status: boolean): Promise<Ocorrencia> {
  const response = await fetch(`${API_URL}/ocorrencias-treino/${ocorrenciaId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao atualizar status da ocorrência de treino.");
  }
  const data = await response.json();
  return data.ocorrencia;
}

export async function deleteOcorrenciaTreinoService(ocorrenciaId: number): Promise<boolean> {
    const response = await fetch(`${API_URL}/ocorrencias-treino/${ocorrenciaId}`, {
        method: "DELETE",
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.erro || "Erro ao remover ocorrência.");
    }
    return response.status === 204;
}