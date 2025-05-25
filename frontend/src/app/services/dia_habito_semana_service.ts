import { DiaSemanaHabito, DiaSemanaInput, MultiDiasSemanaInput } from "@/app/types/dia_semana_habito";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Listar dias de um hábito semanal
export async function listarDiasHabitoSemana(
  habito_id: number
): Promise<DiaSemanaHabito[]> {
  const response = await fetch(
    `${API_URL}/dias-habito-semana/habito/${habito_id}`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao listar dias do hábito semanal");
  }

  return await response.json();
}

// Adicionar um dia ao hábito semanal
export async function adicionarDiaHabitoSemana(
  habito_id: number,
  dia: number
): Promise<DiaSemanaHabito> {
  const response = await fetch(`${API_URL}/dias-habito-semana`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ habito_id, dia }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao adicionar dia ao hábito semanal");
  }

  const data = await response.json();
  return data.dia;
}

// Adicionar vários dias ao hábito semanal
export async function adicionarVariosDiasSemana(
  habito_id: number,
  dias: number[]
): Promise<DiaSemanaHabito[]> {
  const response = await fetch(
    `${API_URL}/dias-habito-semana/habito/${habito_id}/adicionar-varios`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dias }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.erro || "Erro ao adicionar múltiplos dias ao hábito semanal"
    );
  }

  const data = await response.json();
  return data.dias;
}

// Remover dia por ID
export async function removerDiaPorId(dia_id: number): Promise<void> {
  const response = await fetch(`${API_URL}/dias-habito-semana/${dia_id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao remover dia do hábito semanal");
  }
}

// Remover dia por hábito e dia
export async function removerDiaPorHabitoEDia(
  habito_id: number,
  dia: number
): Promise<void> {
  const response = await fetch(
    `${API_URL}/dias-habito-semana/habito/${habito_id}/dia/${dia}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao remover dia do hábito semanal");
  }
}

// Remover todos os dias de um hábito semanal
export async function removerTodosDiasHabitoSemana(
  habito_id: number
): Promise<void> {
  const response = await fetch(
    `${API_URL}/dias-habito-semana/habito/${habito_id}/remover-todos`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      errorData?.erro || "Erro ao remover todos os dias do hábito semanal"
    );
  }
}