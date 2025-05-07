import { Frequencia } from '@/app/types/frequencia'

export interface HabitoUsuario {
    id: number;
    descricao: string;
    frequencia: Frequencia;
    data_inicio: Date;
    vezes_na_semana: number | null;
    usuario_id: number;
    habito_base_id: number;
}