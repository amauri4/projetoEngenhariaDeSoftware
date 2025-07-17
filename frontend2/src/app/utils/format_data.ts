import { formatISO } from 'date-fns';
import { HabitoCreateInput } from '@/app/schemas/HabitoUsuarioSchema';

type HabitoCreateInputAPI = Omit<HabitoCreateInput, 'dataInicio'> & { dataInicio: string };

export function formatHabitForAPI(data: HabitoCreateInput): HabitoCreateInputAPI {
  return {
    ...data,
    dataInicio: formatISO(new Date(data.dataInicio), { representation: 'date' }), // Formato 'YYYY-MM-DD'
  };
}
