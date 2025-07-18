import { RegistroDiario, RegistroDiarioCreateInput, RegistroDiarioUpdateInput } from "@/app/types/registro_habito";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function listarRegistrosUsuario(usuario_id: number): Promise<RegistroDiario[]> {
  const response = await fetch(`${API_URL}/registros-diarios/${usuario_id}/registros`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao listar registros do usuário");
  }

  return await response.json();
}

export async function listarRegistrosConcluidos(usuario_id: number): Promise<RegistroDiario[]> {
  const response = await fetch(`${API_URL}/registros-diarios/${usuario_id}/registros/concluidos`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao listar registros concluídos");
  }

  return await response.json();
}

export async function criarRegistroDiario(data: RegistroDiarioCreateInput): Promise<RegistroDiario> {
  const response = await fetch(`${API_URL}/registros-diarios/registros`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao criar registro diário");
  }

  return await response.json();
}

export async function atualizarRegistroDiario(
  registro_id: number,
  data: RegistroDiarioUpdateInput
): Promise<RegistroDiario> {
  console.log(registro_id)

  const response = await fetch(`${API_URL}/registros-diarios/registros/${registro_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao atualizar registro diário");
  }

  return await response.json();
}

export async function removerRegistroDiario(registro_id: number): Promise<void> {
  const response = await fetch(`${API_URL}/registros-diarios/registros/${registro_id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao remover registro diário");
  }
}

export async function listarRegistrosPorData(
  usuario_id: number,
  data_inicio: string,
  data_fim: string
): Promise<RegistroDiario[]> {
  const params = new URLSearchParams({ data_inicio, data_fim });
  const response = await fetch(
    `${API_URL}/registros-diarios/${usuario_id}/registros/data?${params}`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao listar registros por data");
  }

  return await response.json();
}

export async function listarRegistrosPorDataEspecifica(
  usuario_id: number,
  data: string
): Promise<RegistroDiario[]> {
  const params = new URLSearchParams({ data });
  const response = await fetch(
    `${API_URL}/registros-diarios/${usuario_id}/registros/data_especifica?${params}`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    if (response.status === 400 && errorData?.erro?.includes("Nenhum registro encontrado")) {
      return [];
    }
    throw new Error(errorData?.erro || "Erro ao listar registros por data específica");
  }

  return await response.json();
}