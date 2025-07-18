import { z } from 'zod';

export const TreinoSchema = z.object({
  descricao: z.string().min(3, { message: "A descrição deve ter pelo menos 3 caracteres." }).max(255),
  id_aluno_responsavel: z.coerce.number().min(1, { message: "Selecione um aluno responsável." }),
  data_inicio: z.string().min(1, { message: "A data de início é obrigatória." }),
  data_entrega: z.string().optional(),
}).refine(data => {
  if (data.data_entrega && data.data_inicio) {
    return new Date(data.data_entrega) >= new Date(data.data_inicio);
  }
  return true;
}, {
  message: "A data de entrega não pode ser anterior à data de início.",
  path: ["data_entrega"],
});

export type TreinoCreateInput = z.infer<typeof TreinoSchema>;