import { HabitoUsuario } from "@/app/types/habito_usuario";
import { HabitoCreateInput } from "@/app/schemas/HabitoUsuarioSchema";
import { formatHabitForAPI } from "@/app/utils/format_data"

export async function addHabitService(
  validatedData: HabitoCreateInput
): Promise<HabitoUsuario> {
  validatedData = formatHabitForAPI(validatedData)
  const {
    descricao,
    frequencia,
    dataInicio,
    vezesNaSemana,
    usuarioId,
    habitoBaseId,
  } = validatedData;

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/habitos-usuario/${usuarioId}/habitos`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        descricao,
        habito_base_id: habitoBaseId,
        frequencia,
        data_inicio: dataInicio,
        vezes_na_semana: vezesNaSemana
      }),
    }
  );
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    console.log(dataInicio);
    console.log(errorData)
    throw new Error(
      errorData?.message || "Erro ao adicionar hábito"
    );
  }

  const data = await response.json();
  return data.habito_usuario as HabitoUsuario;
}