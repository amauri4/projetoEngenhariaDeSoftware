"use client";

import { createContext, useState, useContext, ReactNode } from "react";

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (user: User, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const loginUser = (user: User, token: string) => {
    localStorage.setItem("auth_token", token);
    localStorage.setItem("usuario_id", user.id);
    localStorage.setItem("email", user.email);
    setUser(user);
  };

  const logoutUser = () => {
    localStorage.removeItem("auth_token");
    localStorage.removeItem("usuario_id");
    localStorage.removeItem("email");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login: loginUser, logout: logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de AuthProvider");
  }
  return context;
}
