export interface Ocorrencia {
  id: number;
  data: string;
  status: boolean;
  treino_id: number;
  treino_descricao: string;
}

export interface OcorrenciaCreateInput {
  treino_id: number;
  data: string;
  status?: boolean;
}