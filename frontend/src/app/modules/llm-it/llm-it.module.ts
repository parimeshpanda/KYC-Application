import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../../shared/shared.module';
import { NgxSpinnerModule } from 'ngx-spinner';
import { NgbActiveModal, NgbModule, NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
import { ClipboardModule } from '@angular/cdk/clipboard';
import {NgClickOutsideDirective} from 'ng-click-outside2';
import { AngularEditorModule } from '@kolkov/angular-editor';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LlmItComponent } from './llm-it.component';
import { HomeComponent } from './home/home.component';

import { LlmItRoutingModule } from './llm-it-routing.module';
import { ExplanationComponent } from './explanation/explanation.component';
import { PastRecordsComponent } from './past-records/past-records.component';
import { DetailViewComponent } from './detail-view/detail-view.component';
import { MarkdownModule } from 'ngx-markdown';

@NgModule({
  declarations: [
    LlmItComponent,
    LandingPageComponent,
    HomeComponent,
    ExplanationComponent,
    PastRecordsComponent,
    DetailViewComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    AngularEditorModule,
    ReactiveFormsModule,
    SharedModule,
    NgxSpinnerModule,
    NgbModule,
    LlmItRoutingModule,
    ClipboardModule,
    NgClickOutsideDirective,
    NgbPaginationModule,
    MarkdownModule.forRoot()
 
  ],
  providers:[NgbActiveModal]
  
})
export class LlmItModule { }
