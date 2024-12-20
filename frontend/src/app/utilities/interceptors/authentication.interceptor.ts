import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
} from '@angular/common/http';
import { Observable, switchMap, take } from 'rxjs'; 
import { OktaAuthStateService } from "@okta/okta-angular";
import { AuthState } from "@okta/okta-auth-js";
import { okta } from 'src/app/shared/config/app-config';
 

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private oktaAuth: OktaAuthStateService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
  
    return okta ? 
       this.oktaAuth.authState$.pipe(
        take(1), // Take only the first value
        switchMap((authState: AuthState) => {
          const accessToken = authState.accessToken?.accessToken;
          if (accessToken) {
            request = request.clone({
              url: "http://localhost:8000/LLM-IT/" + request.url,
              setHeaders: {
                Authorization: `Bearer ${accessToken}`,
              },
            });
          }
          return next.handle(request);
        })
  ): next.handle(request.clone({ url: "http://localhost:8000/LLM-IT/" + request.url }));
    
    }

    
   
  }
