const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getProdutividadeEquipeInsight(gerenteId: number): Promise<string> {
  const response = await fetch(`${API_URL}/insight2/produtividade-equipe/${gerenteId}`);

  const result = await response.json();

  if (!response.ok || !result.success) {
    throw new Error(result.message || "Erro ao gerar o insight de produtividade.");
  }

  return result.data;
}
