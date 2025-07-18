import { Tarefa } from "@/app/types/tarefa";
import { TarefaCreateInput } from "@/app/schemas/TarefaSchema";

export async function addTarefaService(
  gerenteId: number,
  validatedData: TarefaCreateInput
): Promise<Tarefa> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/tarefas/gerente/${gerenteId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        descricao: validatedData.descricao,
        data_inicio: validatedData.dataInicio,
        responsavel_id: validatedData.responsavelId,
        prazo_final: validatedData.prazoFinal,
      }),
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao adicionar tarefa");
  }

  const data = await response.json();
  return data.tarefa as Tarefa;
}

/**
 * Busca todas as tarefas relacionadas a um ator (gerente ou funcionário).
 */
export async function getTarefasByAtorService(atorId: number): Promise<Tarefa[]> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/tarefas/ator/${atorId}`
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao buscar tarefas");
  }
  return response.json();
}

/**
 * Remove uma tarefa específica.
 */
export async function deleteTarefaService(tarefaId: number): Promise<boolean> {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/tarefas/${tarefaId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao remover tarefa");
  }
  
  // DELETE bem-sucedido geralmente retorna status 204 No Content
  return response.status === 204;
}
