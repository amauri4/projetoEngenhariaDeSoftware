import type { ReactNode } from 'react';
import BottomNavigation from '@/app/components/bottom_nav';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="pb-16"> {/* Espaço para a barra de navegação */}
      {children}
      <BottomNavigation />
    </div>
  );
}