import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { NavbarComponent } from './navbar/navbar.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { OverviewComponent } from './overview/overview.component';
import { LoggedComponent } from './logged/logged.component';
import {RouterModule, Routes} from '@angular/router';
import {AuthInterceptor} from './auth/auth.interceptor';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {UserService} from './shared/user.service';
import { DocumentsListComponent } from './documents-list/documents-list.component';
import { DocumentElementComponent } from './documents-list/document-element/document-element.component';
import {AuthGuardService} from './shared/auth.guard.service';
import { FindDocumentComponent } from './find-document/find-document.component';
import { DocumentNotExistingComponent } from './document-not-existing/document-not-existing.component';
import { DocumentDetailsComponent } from './document-details/document-details.component';
import {RegisterService} from './shared/register.service';

const appRoutes: Routes = [
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'documents', component: FindDocumentComponent, canActivate: [AuthGuardService], children: [
      {path: '-1', component: DocumentNotExistingComponent},
      {path: ':id', component: DocumentDetailsComponent}
    ]}
];

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    LoginComponent,
    RegisterComponent,
    OverviewComponent,
    LoggedComponent,
    DocumentsListComponent,
    DocumentElementComponent,
    FindDocumentComponent,
    DocumentNotExistingComponent,
    DocumentDetailsComponent,
    LoggedComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes),
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    HttpClientModule,
    UserService,
    AuthGuardService,
    RegisterService,
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
