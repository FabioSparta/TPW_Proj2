import {Injectable, Injector} from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import {AuthService} from "../../_services/auth.service";

@Injectable()
export class AuthHeaderInterceptor implements HttpInterceptor{

  constructor(private injector: Injector) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const authService = this.injector.get(AuthService);
    if (authService.isAuthenticated()){
      const tokenizedReq = req.clone({
        setHeaders: {Authorization: `Token ${authService.getToken()}`}
      });
      return next.handle(tokenizedReq);
    }
    return next.handle(req);
  }

}
