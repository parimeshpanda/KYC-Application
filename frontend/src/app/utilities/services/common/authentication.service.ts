import { Inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { RestService } from '../rest.service';
import { NgxSpinnerService } from 'ngx-spinner';
import { HttpClient } from '@angular/common/http';

import { OKTA_AUTH, OktaAuthStateService } from "@okta/okta-angular";
import OktaAuth from "@okta/okta-auth-js";
import { okta } from 'src/app/shared/config/app-config';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  public currentUser: BehaviorSubject<any> = new BehaviorSubject<any>(null);
  public isAuthenticated$: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);


  constructor(
    private restService: RestService,
    private spinner: NgxSpinnerService,
    private http: HttpClient,
    @Inject(OKTA_AUTH) private oktaAuth: OktaAuth,
    private _oktaStateService: OktaAuthStateService
  ) {

  }

  public getUserInfo() {
    return this.currentUser.asObservable();
  }

  public authenticate(okta: boolean, userInfo: any): any { 
      let url = 'home/getUserDetails';
      return this.restService.postData(url, userInfo);
  }

  /**
   * @description 
   * okta login info
   */
  public async loadUserInfo(okta: any) {
    if (okta) {
      let userInfo = await this.oktaAuth.getUser();
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
      let data = {
        email: userInfo.email,
        family_name: userInfo.family_name,
        given_name: userInfo.given_name,
        preferred_username: userInfo.preferred_username

      }

      this.authenticate(okta, data).subscribe((user: any) => {
        if (user && okta) {
          localStorage.setItem('userInfo', JSON.stringify(user['data'][0]))
          this.currentUser.next(user['data'][0]);
        }
      });
    } else {
      setTimeout(() => {
        this.getUserDetailsDev();
      }, 1500);
    } 
  }

  /**
  * @description Get & Set Current User  :: Dev modeapp-r
  *
  * @param 
  * @memberof User Authentication
  */

  public getUserDetailsDev() {

    let user = {
      "status": 200, "message": "SUCCESS", "data": [{
        "id": "664b484926fe48c59863cf68",
        "emailId": "john.doe@genpact.com",
        "userName": "John Doe",
        "lastLogin": "2024-05-20T12:55:57.695237",
        "password": null,
        "roleId": 1,
        "isAdmin": true,
        "firstname": "John",
        "lastname": "Doe",
        "ohrId": 703253266
      }]
    };
    if (user) {
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      localStorage.setItem('userInfo', JSON.stringify(user['data'][0]));
      this.currentUser.next(user['data'][0]);
    }

  }



}
