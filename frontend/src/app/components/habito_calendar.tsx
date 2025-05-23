"use client";

import { format, parseISO } from "date-fns";
import { useEffect, useState } from "react";

export interface HabitCalendarProps {
  selectedDate: Date;
  onDateChange: (date: Date) => void;
  minDate?: Date;
  maxDate?: Date;
}

export default function HabitCalendar({
  selectedDate,
  onDateChange,
  minDate,
  maxDate,
}: HabitCalendarProps) {
  const [inputValue, setInputValue] = useState(
    format(selectedDate, "yyyy-MM-dd")
  );

  useEffect(() => {
    setInputValue(format(selectedDate, "yyyy-MM-dd"));
  }, [selectedDate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    
    try {
      const date = value ? parseISO(value) : new Date();
      
      if (isNaN(date.getTime())) {
        console.error("Data inválida selecionada");
        return;
      }

      if (minDate && date < minDate) {
        console.warn("Data selecionada é anterior à data mínima permitida");
        return;
      }

      if (maxDate && date > maxDate) {
        console.warn("Data selecionada é posterior à data máxima permitida");
        return;
      }

      onDateChange(date);
    } catch (error) {
      console.error("Erro ao processar data:", error);
    }
  };

  return (
    <div className="my-4">
      <label htmlFor="habit-date" className="block text-sm text-gray-600 mb-1">
        Selecionar data
      </label>
      <input
        id="habit-date"
        type="date"
        value={inputValue}
        onChange={handleChange}
        min={minDate ? format(minDate, "yyyy-MM-dd") : undefined}
        max={maxDate ? format(maxDate, "yyyy-MM-dd") : undefined}
        className="border border-gray-300 p-2 rounded-lg w-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
      />
    </div>
  );
}