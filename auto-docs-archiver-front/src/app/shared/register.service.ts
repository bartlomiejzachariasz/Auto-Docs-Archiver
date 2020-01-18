import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {UserLogin} from './user.login';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  private API = 'http://localhost:8000/auth/register';

  constructor(private http: HttpClient) {
  }

  save(user: UserLogin): Observable<UserLogin> {
    return this.http.post<UserLogin>(this.API, user);
  }


}
