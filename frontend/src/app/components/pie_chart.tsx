import { PieChart as RechartsPie, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface PieData {
  name: string;
  value: number;
  color: string;
}

export default function PieChart({ data }: { data: PieData[] }) {
  const hasData = data && data.length > 0;

  return (
    <ResponsiveContainer width="100%" height="100%">
      { hasData ?
        <RechartsPie>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => [`${value}%`, 'Porcentagem']} />
          <Legend />
        </RechartsPie>
      : (
        <p style={{ fontSize: 16, color: '#888' }}>Nenhum dado disponível para exibir o gráfico.</p>
      )}
    </ResponsiveContainer>
  );
}