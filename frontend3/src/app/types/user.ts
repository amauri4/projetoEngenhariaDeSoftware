export interface AuthenticatedUser {
    id: number;
    nome: string;
    email: string;
    tipo_ator: 'gerente' | 'funcionario';
    chefe_id?: number | null; 
  }

  export interface RegistrationData {
    nome: string;
    email: string;
    senha: string;
    chefe_id?: number | null;
  }
  
  export interface LoginData {
    email: string;
    senha: string;
  }
  