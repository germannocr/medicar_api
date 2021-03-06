import { HttpErrorResponse, HttpHeaders, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';

import { TokenStorageService } from '../_services/token-storage.service';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

const TOKEN_HEADER_KEY = 'Authorization';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private token: TokenStorageService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    
    let authReq = req;
    const token = this.token.getToken();
    if (token != null) {
      const headers = new HttpHeaders({
        'Authorization': `JWT ${token}`,
        'Content-Type': 'application/json'
      });
      authReq = req.clone({headers});
    }
    return next.handle(authReq)
  }
}

export const authInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
];