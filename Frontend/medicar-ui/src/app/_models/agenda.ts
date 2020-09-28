import { Time } from '@angular/common';
import { Medico } from './medico';

export interface Agenda {
    id: number;
    medico: Medico;
    dia: Date;
    horarios: Time[];
}
