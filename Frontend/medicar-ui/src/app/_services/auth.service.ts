import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

const AUTH_API = 'http://localhost:8000';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  login(credentials): Observable<any> {
    return this.http.post(AUTH_API + '/login/', {
      username: credentials.username,
      password: credentials.password
    })
  }

  register(user): Observable<any> {
    return this.http.post(AUTH_API + '/registration/', {
      username: user.username,
      email: user.email,
      password1: user.password1,
      password2: user.password2
    })
  }

}