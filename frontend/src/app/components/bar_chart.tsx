import { BarChart as RechartsBar, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface BarData {
  name: string;
  completion: number;
}

export default function BarChart({ data }: { data: BarData[] }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <RechartsBar data={data}>
        <XAxis dataKey="name" />
        <YAxis domain={[0, 100]} />
        <Tooltip formatter={(value) => [`${value}%`, 'Conclusão']} />
        <Bar dataKey="completion" fill="#7C3AED" radius={[4, 4, 0, 0]} />
      </RechartsBar>
    </ResponsiveContainer>
  );
}