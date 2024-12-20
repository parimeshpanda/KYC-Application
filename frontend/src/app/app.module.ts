
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgxSpinnerModule } from 'ngx-spinner';
import { SharedModule } from './shared/shared.module';
import { AuthGuard } from './utilities/guards/auth.guard';
import { HIGHLIGHT_OPTIONS, HighlightModule } from 'ngx-highlightjs';
import { OktaAuthModule, OKTA_CONFIG } from '@okta/okta-angular';
import { OktaAuth } from '@okta/okta-auth-js'; 
import { environment } from 'src/environments/environment';
import { AuthInterceptor } from './utilities/interceptors/authentication.interceptor';
import { prod } from './shared/config/app-config';


const oktaAuth = new OktaAuth({
  issuer: environment.issuer,
  clientId: environment.clientId,
  redirectUri: environment.redirectUri
});
@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    SharedModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    HighlightModule,
    NgxSpinnerModule,
    OktaAuthModule,
  ],
  providers:[AuthGuard,{
    provide: HIGHLIGHT_OPTIONS,
    useValue: {
      fullLibraryLoader: () => import('highlight.js/lib/core'),
      lineNumbersLoader: () => import('ngx-highlightjs/line-numbers'), // Optional, only if you want the line numbers
    }
  },{ 
    provide: OKTA_CONFIG, 
    useValue: { oktaAuth } 
  } , {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true,
  },],
  bootstrap: [AppComponent]
})
export class AppModule { }
