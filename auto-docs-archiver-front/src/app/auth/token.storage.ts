import {Injectable} from '@angular/core';

@Injectable({providedIn: 'root'})
export class TokenStorage {

  constructor() {
  }

  private TOKEN_KEY = 'AuthToken';
  private USERNAME_KEY = 'AuthUsername';
  private AUTHORITIES_KEY = 'AuthAuthorities';

  public saveToken(token: string) {
    window.sessionStorage.removeItem(this.TOKEN_KEY);
    window.sessionStorage.setItem(this.TOKEN_KEY, token);
  }

  public getToken() {
    return window.sessionStorage.getItem(this.TOKEN_KEY);
  }

  public saveUsername(username: string) {
    window.sessionStorage.removeItem(this.USERNAME_KEY);
    window.sessionStorage.setItem(this.USERNAME_KEY, username);
  }

  public getUsername() {
    return window.sessionStorage.getItem(this.USERNAME_KEY);
  }

  public logout() {
    window.sessionStorage.clear();
  }

}
