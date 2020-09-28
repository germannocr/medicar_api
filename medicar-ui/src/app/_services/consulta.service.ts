import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { Consulta } from '../_models/consulta';
import { Medico } from '../_models/medico';
import { Especialidade } from '../_models/especialidade';
import { AbstractControl } from '@angular/forms';
import { Agenda } from '../_models/agenda';

@Injectable({
  providedIn: 'root'
})
export class ConsultaService {

  url = 'http://localhost:8000/'

  constructor(private httpClient: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  }

  getConsultaList(): Observable<Consulta[]> {
    return this.httpClient.get<Consulta[]>(`${this.url}retrieve_consultas/`).pipe(
      retry(2),
      catchError(this.handleError)
    )
  }

  getMedicoList(especialidade: number): Observable<Medico[]> {
    return this.httpClient.get<Medico[]>(`${this.url}retrieve_medicos/?especialidade=${especialidade}`).pipe(
      retry(2),
      catchError(this.handleError)
    )
  }

  getAgendaList(especialidade: AbstractControl, medico: AbstractControl): Observable<Agenda[]> {
    return this.httpClient.get<Agenda[]>(`${this.url}retrieve_agendas/?especialidade=${especialidade}&medico=${medico}`).pipe(
      retry(2),
      catchError(this.handleError)
    )
  }

  getAgendaListByDate(date: AbstractControl, especialidade: AbstractControl, medico: AbstractControl): Observable<Agenda[]> {
    return this.httpClient.get<Agenda[]>(`${this.url}retrieve_agendas/?especialidade=${especialidade}&medico=${medico}&data_inicio=${date}&data_final=${date}`).pipe(
      retry(2),
      catchError(this.handleError)
    )
  }

  getEspecialidadeList(): Observable<Especialidade[]> {
    return this.httpClient.get<Especialidade[]>(`${this.url}retrieve_especialidades/`).pipe(
      retry(2),
      catchError(this.handleError)
    )
  }

  addConsulta(consulta: Consulta): Observable<Consulta> {
    return this.httpClient.post<Consulta>(
        `${this.url}create_consulta/`,
        JSON.stringify(consulta), 
        this.httpOptions
      ).pipe(
        retry(2),
        catchError(this.handleError)
      )
  }

  deleteConsulta(consulta: Consulta) {
    return this.httpClient.delete<Consulta>(
      `${this.url}delete_consulta/${consulta.id}`,
      this.httpOptions
    ).pipe(
      retry(1),
      catchError(this.handleError)
    )
  }

  handleError(error: HttpErrorResponse) {
    let errorMessage = '';
    // Client error
    if (error.error instanceof ErrorEvent) {
      errorMessage = error.error.message;
    } else {
      // Server error
      errorMessage = `Error code: ${error.status}, ` + `message: ${error.message}`;
    }
    console.log(errorMessage);
    return throwError(errorMessage);
  };
}
