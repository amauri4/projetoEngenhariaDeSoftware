"use client";

import { format } from "date-fns";

export interface HabitCalendarProps {
  selectedDate: Date;
  onDateChange: (date: Date) => void;
}

export default function HabitCalendar({ selectedDate, onDateChange }: HabitCalendarProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onDateChange(new Date(e.target.value));
  };

  return (
    <div className="my-4">
      <label className="block text-sm text-gray-600 mb-1">Selecionar data</label>
      <input
        type="date"
        value={format(selectedDate, "yyyy-MM-dd")}
        onChange={handleChange}
        className="border border-gray-300 p-2 rounded-lg w-full"
      />
    </div>
  );
}
