import { z } from 'zod';
import { Frequencia } from '@/app/types/frequencia';

export const HabitoUsuarioSchema = z.object({
  habitoBaseId: z.number().int().positive(),
  descricao: z.string().max(255),
  frequencia: z.nativeEnum(Frequencia),
  dataInicio: z.coerce.date(),
  vezesNaSemana: z.number().int().min(1).max(7).nullable().optional(),
  usuarioId: z.number().int().positive(),
});

export type HabitoCreateInput = z.infer<typeof HabitoUsuarioSchema>;