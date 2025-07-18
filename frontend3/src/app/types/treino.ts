export interface Treino {
  id: number;
  descricao: string;
  data_inicio: string;
  data_entrega?: string | null;
  criador_id: number;
  criador_nome?: string | null;
  responsavel_id: number;
  responsavel_nome?: string | null;
}

export interface TreinoCreateInput {
  descricao: string;
  data_inicio: string;
  id_aluno_responsavel: number;
  data_entrega?: string | null;
}