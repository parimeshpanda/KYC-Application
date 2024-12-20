import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/common/authentication.service';
import { okta } from 'src/app/shared/config/app-config';

@Injectable()
export class RouteResolver implements Resolve<any> {
  constructor(
    private authenticate : AuthService,
  ) {}
  private okta = okta;
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    return this.getResolverData(route.data);
  }
  public  async getResolverData(data: any): Promise<any> {
    switch (data.for) {
      case "LoginData": 
        await this.authenticate.loadUserInfo(okta)
        break
      default:
        break;
    }
  }
}
