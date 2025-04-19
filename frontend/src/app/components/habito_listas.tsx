"use client";

export interface HabitListProps {
  habits: string[];
  onRemove: (index: number) => void;
}

export default function HabitList({ habits, onRemove }: HabitListProps) {
  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Seus hábitos do dia</h2>
      {habits.length === 0 ? (
        <p className="text-sm text-gray-500">Nenhum hábito adicionado.</p>
      ) : (
        <ul className="space-y-2">
          {habits.map((habit, index) => (
            <li
              key={index}
              className="flex justify-between items-center bg-gray-100 p-2 rounded-lg"
            >
              <span>{habit}</span>
              <button
                onClick={() => onRemove(index)}
                className="text-red-500 hover:underline text-sm"
              >
                Remover
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
