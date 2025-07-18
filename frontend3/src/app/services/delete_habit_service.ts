export async function deleteHabitoUsuario(habitoUsuarioId: number): Promise<void> {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/habitos-usuario/habitos/${habitoUsuarioId}`,
      {
        method: "DELETE",
      }
    );
  
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.erro || "Erro ao remover hábito");
    }
  }
  