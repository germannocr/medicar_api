import { Especialidade } from './especialidade'

export interface Medico {
    id: number;
    nome: string;
    crm: number;
    email: string;
    telefone: string;
    especialidade: Especialidade;
}
