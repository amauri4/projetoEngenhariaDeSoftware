export enum Frequencia {
    DIARIA = "diaria",
    SEMANAL = "semanal",
    MENSAL = "mensal"
  }
  
export type FrequenciaType = keyof typeof Frequencia;