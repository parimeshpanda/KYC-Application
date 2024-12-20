
import { Component, Inject } from '@angular/core';
import { BnNgIdleService } from 'bn-ng-idle';
import { OKTA_AUTH } from '@okta/okta-angular';
import OktaAuth from '@okta/okta-auth-js';
import { environment } from 'src/environments/environment';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  public baseurl: string = environment.baseurl = '';
  constructor(private bnIdle: BnNgIdleService,@Inject(OKTA_AUTH) private oktaAuth: OktaAuth) {
   //logout if idle after 15 minutes
   this.bnIdle.startWatching(1200).subscribe(async (isTimedOut: boolean) => {
    if (isTimedOut) {

        await this.oktaAuth.signOut({
          postLogoutRedirectUri: environment.postLogoutRedirectUri
        })
        localStorage.clear();
      
    }
  });
  window.onbeforeunload = function (e: any) {
    if ("caches" in window) {
      caches.keys().then(function (keyList) {
        return Promise.all(
          keyList.map(function (key) {
            return caches.delete(key);
          })
        );
      });
    }
  };
   
  }

}

