import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppNoSpecialCharactersDirective } from './directives/nospecialcharacters';
import { AppNowhitespaceDirective } from './directives/nowhitespace.directive';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ScrollSpyDirective } from './directives/scroll-spy.directive';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SanitizedHtmlPipe } from './pipes/search.pipe';
import { ToastsComponent } from './toasts/toasts.component';


@NgModule({
  declarations: [
    SanitizedHtmlPipe,
    AppNoSpecialCharactersDirective,
    AppNowhitespaceDirective,
    HeaderComponent,
    FooterComponent,
    ScrollSpyDirective,
    ToastsComponent
  ],
  imports: [
    CommonModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  exports: [
    SanitizedHtmlPipe,
    AppNoSpecialCharactersDirective,
    AppNowhitespaceDirective,
    HeaderComponent,
    FooterComponent,
    ScrollSpyDirective,
    ToastsComponent
  ]
})
export class SharedModule { }
