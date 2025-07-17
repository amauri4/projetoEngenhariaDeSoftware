export interface Tarefa {
    id: number;
    descricao: string;
    data_inicio: string;
    prazo_final?: string | null;
    criador_id: number;
    criador_nome?: string | null;
    responsavel_id: number;
    responsavel_nome?: string | null;
  }
  