import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LlmItComponent } from './llm-it.component';
import { HomeComponent } from './home/home.component';
import { OktaAuthGuard } from '@okta/okta-angular';
import { okta } from 'src/app/shared/config/app-config';
import { AuthGuard } from 'src/app/utilities/guards/auth.guard';
import { ExplanationComponent } from './explanation/explanation.component';
import { PastRecordsComponent } from './past-records/past-records.component';
import { DetailViewComponent } from './detail-view/detail-view.component';

const routes: Routes = [
  {
    path: '',
    component: LlmItComponent,
    //canActivate:[okta? OktaAuthGuard :AuthGuard],
    children : [
      {
        path:'',
        // redirectTo : 'home',
        pathMatch: 'full',
        component: LandingPageComponent,
      },
      {
        path: 'home',
        component: HomeComponent,
        canActivate:[okta? OktaAuthGuard :AuthGuard]
      },
      {
        path: 'explanation',
        component: ExplanationComponent,
        canActivate:[okta? OktaAuthGuard :AuthGuard]
      },
      {
        path: 'past-records',
        component: PastRecordsComponent,
        canActivate:[okta? OktaAuthGuard :AuthGuard]
      },
      {
        path: 'detail-view',
        component: DetailViewComponent,
        canActivate:[okta? OktaAuthGuard :AuthGuard]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LlmItRoutingModule { }
