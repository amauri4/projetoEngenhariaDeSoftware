import { BarChart as RechartsBar, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface ProgressData {
  day: string;
  completed: number;
  total: number;
}

interface ChartData extends ProgressData {
  percentage: number;
}

export default function ProgressChart({ data }: { data: ProgressData[] }) {
  const chartData: ChartData[] = data.map(item => ({
    day: item.day,
    completed: item.completed,
    total: item.total,
    percentage: (item.completed / item.total) * 100
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsBar data={chartData}>
        <XAxis dataKey="day" />
        <YAxis domain={[0, 100]} />
        <Tooltip 
          formatter={(value: number, name: string) => {
            if (name === 'percentage') {
              return [`${value.toFixed(1)}%`, 'Conclusão'];
            }
            return [value, name === 'completed' ? 'Completos' : 'Total'];
          }} 
        />
        <ReferenceLine y={100} stroke="#E9D5FF" strokeDasharray="3 3" />
        <Bar dataKey="percentage" fill="#8B5CF6" name="Conclusão" radius={[4, 4, 0, 0]} />
      </RechartsBar>
    </ResponsiveContainer>
  );
}