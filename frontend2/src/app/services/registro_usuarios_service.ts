import { AuthenticatedUser, RegistrationData, LoginData } from "@/app/types/user";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * Registra um novo Gerente.
 * @param data - Os dados de registro (nome, email, senha).
 * @returns O objeto do gerente criado.
 */
export async function registerGerenteService(data: RegistrationData): Promise<{ mensagem: string; gerente: AuthenticatedUser }> {
  const response = await fetch(`${API_URL}/auth/gerentes/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao registrar gerente.");
  }

  return response.json();
}

/**
 * Autentica um Gerente.
 * @param credentials - As credenciais de login (email, senha).
 * @returns O objeto do gerente autenticado.
 */
export async function loginGerenteService(credentials: LoginData): Promise<AuthenticatedUser> {
  const response = await fetch(`${API_URL}/auth/gerentes/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Credenciais de gerente inválidas.");
  }

  return response.json();
}

/**
 * Registra um novo Funcionário.
 * @param data - Os dados de registro (nome, email, senha, chefe_id opcional).
 * @returns O objeto do funcionário criado.
 */
export async function registerFuncionarioService(data: RegistrationData): Promise<{ mensagem: string; funcionario: AuthenticatedUser }> {
  const response = await fetch(`${API_URL}/auth/funcionarios/registrar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Erro ao registrar funcionário.");
  }

  return response.json();
}

/**
 * Autentica um Funcionário.
 * @param credentials - As credenciais de login (email, senha).
 * @returns O objeto do funcionário autenticado.
 */
export async function loginFuncionarioService(credentials: LoginData): Promise<AuthenticatedUser> {
  const response = await fetch(`${API_URL}/auth/funcionarios/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.erro || "Credenciais de funcionário inválidas.");
  }

  return response.json();
}
