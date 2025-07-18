export function numeroParaDia(dayNumber: number): string {
    const dias = [
      "domingo",
      "segunda",
      "terca",
      "quarta",
      "quinta",
      "sexta",
      "sabado"
    ];
  
    if (dayNumber < 0 || dayNumber > 6) {
      throw new Error("Número do dia deve estar entre 0 e 6");
    }
  
    return dias[dayNumber];
  }