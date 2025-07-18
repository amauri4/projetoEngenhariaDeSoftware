export interface LoginFormData {
    email: string;
    senha: string;
  }
  
  export async function login(formData: LoginFormData) {
    const LOGIN_ROUTE = `${process.env.NEXT_PUBLIC_API_URL}/auth1/login`;
  
    const response = await fetch(LOGIN_ROUTE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
  
    const data = await response.json();
  
    if (!response.ok) {
      throw new Error(data.erro || "Credenciais inválidas");
    }
  
    return data;
  }
  