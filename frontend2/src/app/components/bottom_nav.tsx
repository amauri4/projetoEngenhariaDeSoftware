"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FaChartLine, FaRobot, FaCalendarAlt, FaList } from "react-icons/fa";

export default function BottomNavigation() {
    const pathname = usePathname();

    return (
        <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
            <div className="flex justify-around items-center h-16">
                <Link
                    href="/dashboard"
                    className={`flex flex-col items-center justify-center w-full h-full ${pathname === '/dashboard' ? 'text-purple-600' : 'text-gray-500'}`}
                >
                    <FaList className="text-xl" />
                    <span className="text-xs mt-1">Lista</span>
                </Link>

                <Link
                    href="/dashboard/chat"
                    className={`flex flex-col items-center justify-center w-full h-full ${pathname === '/chat' ? 'text-purple-600' : 'text-gray-500'}`}
                >
                    <div className="relative">
                        <FaRobot className="text-xl" />
                        {pathname === '/chat' && (
                            <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-purple-500"></span>
                        )}
                    </div>
                    <span className="text-xs mt-1">SecretarIA</span>
                </Link>

                {/* <Link
                    href="/dashboard/calendario"
                    className={`flex flex-col items-center justify-center w-full h-full ${pathname === '/dashboard/calendario' ? 'text-purple-600' : 'text-gray-500'}`}
                >
                    <FaCalendarAlt className="text-xl" />
                    <span className="text-xs mt-1">Calendário</span>
                </Link> */}
            </div>
        </nav>
    );
}