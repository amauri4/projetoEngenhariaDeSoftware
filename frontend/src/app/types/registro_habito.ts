export type RegistroDiario = {
    id: number;
    data: string; // Date se converter
    habito_id: number;
    concluido: boolean;
  };
  
  export type RegistroDiarioCreateInput = {
    data: string;
    habito_id: number;
    concluido?: boolean;
  };
  
  export type RegistroDiarioUpdateInput = {
    concluido: boolean;
  };