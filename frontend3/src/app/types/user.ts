export interface AuthenticatedUser {
    id: number;
    nome: string;
    email: string;
    tipo_ator: 'instrutor' | 'aluno';
    instrutor_id?: number | null; 
  }

  export interface RegistrationData {
    nome: string;
    email: string;
    senha: string;
    instrutor_id?: number | null;
  }
  
  export interface LoginData {
    email: string;
    senha: string;
  }
  