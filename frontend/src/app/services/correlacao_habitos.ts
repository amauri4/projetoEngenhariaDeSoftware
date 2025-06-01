const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const buscarCorrelacoesHabitos = async (usuarioId: number): Promise<string> => {
    try {
        const response = await fetch(
            `${API_URL}/operacoes-extra/correlacoes/${usuarioId}`,
            {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new Error(errorData?.message || "Erro ao buscar correlações entre hábitos");
        }

        const responseData = await response.json();
        
        if (responseData.success && typeof responseData.data === 'string') {
            return responseData.data;
        }
        
        throw new Error("Formato de resposta inesperado da API");
    } catch (error) {
        console.error('Erro no service ao buscar correlações:', error);
        throw error instanceof Error ? error : new Error("Erro desconhecido ao buscar correlações");
    }
};