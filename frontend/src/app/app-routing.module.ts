
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RouteResolver } from './utilities/resolvers/data-resolvers';
import { OktaAuthGuard, OktaCallbackComponent } from '@okta/okta-angular';

const routes: Routes = [
  { path: 'login/callback', component: OktaCallbackComponent },
  {
    path:'',
    loadChildren:()=> import('./modules/llm-it/llm-it.module').then(mod => mod.LlmItModule),
    resolve: { data: RouteResolver}, 
    // canActivate:[OktaAuthGuard],
    data: { for: "LoginData" }
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers:[RouteResolver]
})
export class AppRoutingModule { }
