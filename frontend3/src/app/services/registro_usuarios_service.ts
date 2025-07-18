import { AuthenticatedUser, RegistrationData, LoginData } from "@/app/types/user";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function registerInstrutorService(data: RegistrationData): Promise<{ mensagem: string; instrutor: AuthenticatedUser }> {
  const response = await fetch(`${API_URL}/auth3/instrutores/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao registrar instrutor.");
  }
  return response.json();
}

export async function loginInstrutorService(credentials: LoginData): Promise<AuthenticatedUser> {
  const response = await fetch(`${API_URL}/auth3/instrutores/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Credenciais de instrutor inválidas.");
  }
  return response.json();
}

export async function registerAlunoService(data: RegistrationData): Promise<{ mensagem: string; aluno: AuthenticatedUser }> {
  const response = await fetch(`${API_URL}/auth3/alunos/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao registrar aluno.");
  }
  return response.json();
}

export async function loginAlunoService(credentials: LoginData): Promise<AuthenticatedUser> {
  const response = await fetch(`${API_URL}/auth3/alunos/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Credenciais de aluno inválidas.");
  }
  return response.json();
}