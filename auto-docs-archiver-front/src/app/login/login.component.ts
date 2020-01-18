import {Component, OnInit, Output} from '@angular/core';
import {EventEmitter} from 'events';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {TokenStorage} from '../auth/token.storage';
import {UserService} from '../shared/user.service';
import {UserLogin} from '../shared/user.login';
import {JwtResponse} from '../auth/jwt.response';
import {User} from '../shared/user';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  @Output() loginEmitter = new EventEmitter();
  private API = 'http://localhost:8000';
  private LOGIN_API = this.API + '/auth/signin';

  loginForm: FormGroup;
  loginFailed = false;

  constructor(private http: HttpClient, private router: Router,
              private tokenStorage: TokenStorage, private userService: UserService) {
  }

  private logIn(userLogin: UserLogin) {
    this.http.post<JwtResponse>(this.LOGIN_API, userLogin).subscribe(
      data => {
        this.tokenStorage.saveToken(data.token);
        this.tokenStorage.saveUsername(data.username);
        this.userService.user = new User(this.tokenStorage.getUsername());

        this.loginFailed = false;
        this.loginEmitter.emit(null);
        this.router.navigate(['/documents']);
      },
      error => {
        this.loginFailed = true;
        this.loginForm.get('password').setValue('');
      }
    );
  }

  submitForm() {
    const userLogin = new UserLogin(this.loginForm.get('username').value, this.loginForm.get('password').value);
    this.logIn(userLogin);
  }

  ngOnInit() {
    this.loginForm = new FormGroup({
      'username': new FormControl(null, Validators.required),
      'password': new FormControl(null, Validators.required)
    });
  }


}
