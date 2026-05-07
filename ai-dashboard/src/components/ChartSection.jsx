import { BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

export default function ChartSection({ data }) {
  return (
    <BarChart width={500} height={300} data={data}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="value" fill="#8884d8" />
    </BarChart>
  );
}