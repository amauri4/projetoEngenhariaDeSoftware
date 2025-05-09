import { Frequencia } from '@/app/types/frequencia';

export interface HabitoUsuario {
    id: number;
    descricao: string;
    frequencia: Frequencia;
    data_inicio: Date;
    vezes_na_semana: number | null;
    dias_semana: number[] | null; // Array com índices dos dias (0-6, onde 0=Domingo)
    dias_mes: number[] | null;   // Array com dias do mês (1-31)
    usuario_id: number;
    habito_base_id: number;
}

// Tipo para o payload da API
export interface HabitoPayload {
    descricao: string;
    frequencia: Frequencia;
    data_inicio: string;         // Formato ISO (YYYY-MM-DD)
    vezes_na_semana?: number | null;
    dias_semana?: number[];
    dias_mes?: number[];
    usuario_id: number;
    habito_base_id: number;
}

// Tipos auxiliares para os dias
export type DiaSemana = 0 | 1 | 2 | 3 | 4 | 5 | 6; // 0=Domingo, 1=Segunda, etc.
export type DiaMes = 
  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10
  | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20
  | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30
  | 31;

export interface HabitoFormInput {
    habito_base_id: number;
    descricao: string;
    frequencia: Frequencia;
    data_inicio: string; // Formato ISO (YYYY-MM-DD)
    vezes_na_semana?: number | null;
    dias_semana_selecionados: number[];
    dias_mes_selecionados: number[];
}