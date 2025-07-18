import { z } from 'zod';

export const TarefaSchema = z.object({
  descricao: z.string()
    .min(3, { message: "A descrição deve ter pelo menos 3 caracteres." })
    .max(255, { message: "A descrição não pode exceder 255 caracteres." }),
  
  responsavelId: z.coerce.number({
      invalid_type_error: "Selecione um funcionário responsável.",
    })
    .min(1, { message: "Selecione um funcionário responsável." }),
  
  dataInicio: z.string()
    .min(1, { message: "A data de início é obrigatória." }),
    
  prazoFinal: z.string()
    .optional()
    .transform(val => (val === "" ? undefined : val)), // Transforma string vazia em undefined para o optional funcionar corretamente
    
}).refine(data => {
  // Garante que o prazo final não seja anterior à data de início
  if (data.prazoFinal && data.dataInicio) {
    return new Date(data.prazoFinal) >= new Date(data.dataInicio);
  }
  return true;
}, {
  message: "O prazo final não pode ser anterior à data de início.",
  path: ["prazoFinal"], // Associa o erro ao campo do prazo final
});

export type TarefaCreateInput = z.infer<typeof TarefaSchema>;
