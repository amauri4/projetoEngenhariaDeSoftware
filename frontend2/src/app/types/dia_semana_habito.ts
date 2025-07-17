export type DiaSemanaHabito = {
    id: number;
    habito_id: number;
    dia: number; 
  };
  
  export type DiaSemanaInput = {
    dia: number;
  };
  
  export type MultiDiasSemanaInput = {
    dias: number[];
  };