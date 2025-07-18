import { z } from 'zod';
import { Frequencia } from '@/app/types/frequencia';

export const HabitoUsuarioSchema = z.object({
  habitoBaseId: z.number().int().positive(),
  descricao: z.string()
    .min(3, "Descrição muito curta (mínimo 3 caracteres)")
    .max(255, "Descrição muito longa (máximo 255 caracteres)"),
  frequencia: z.nativeEnum(Frequencia),
  dataInicio: z.string()
    .regex(/^\d{4}-\d{2}-\d{2}$/, "Formato de data inválido. Use YYYY-MM-DD")
    .refine(val => !isNaN(new Date(val).getTime()), { message: "Data inválida" }),
  vezesNaSemana: z.number()
    .int()
    .min(1, "Mínimo 1 vez por semana")
    .max(7, "Máximo 7 vezes por semana")
    .nullable()
    .optional(),
  diasSemana: z.array(
    z.number()
      .int()
      .min(1, "Dia inválido")
      .max(7, "Dia inválido")
  ).optional(),
  diasMes: z.array(
    z.number()
      .int()
      .min(1, "Dia inválido")
      .max(31, "Dia inválido")
  ).optional(),
  usuarioId: z.number().int().positive()
}).superRefine((data, ctx) => {
  // Validação condicional para frequência semanal
  if (data.frequencia === Frequencia.SEMANAL && data.vezesNaSemana === null) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Necessário para frequência semanal",
      path: ["vezesNaSemana"]
    });
  }

  // Validação condicional para frequência diária
  if (data.frequencia === Frequencia.DIARIA && (!data.diasSemana || data.diasSemana.length === 0)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Selecione pelo menos um dia da semana",
      path: ["diasSemana"]
    });
  }

  // Validação condicional para frequência mensal
  if (data.frequencia === Frequencia.MENSAL && (!data.diasMes || data.diasMes.length === 0)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Selecione pelo menos um dia do mês",
      path: ["diasMes"]
    });
  }

  // Validação para evitar vezesNaSemana quando não é semanal
  if (data.frequencia !== Frequencia.SEMANAL && data.vezesNaSemana !== null) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Não deve ser preenchido para esta frequência",
      path: ["vezesNaSemana"]
    });
  }
})

export type HabitoCreateInput = z.infer<typeof HabitoUsuarioSchema>;