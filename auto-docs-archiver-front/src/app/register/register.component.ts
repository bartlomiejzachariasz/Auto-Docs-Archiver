import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {User} from '../shared/user';
import {UserLogin} from '../shared/user.login';
import {RegisterService} from '../shared/register.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  invalidForm = false;
  userExists: boolean;
  passwordMatch: boolean;
  userRegistered = false;


  constructor(private registerService: RegisterService) {
    this.registerForm = new FormGroup({
      'username': new FormControl(null, [Validators.required, Validators.min(3), Validators.max(10)]),
      'password': new FormControl(null, [Validators.min(5)]),
      'rPassword': new FormControl(null, [Validators.required]),
    });
  }

  ngOnInit() {

  }

  validate(password: string, rPassword: string) {
    return password === rPassword;
  }

  registerUser() {
    const username = this.registerForm.get('username').value;
    const password = this.registerForm.get('password').value;
    const rPassword = this.registerForm.get('rPassword').value;
    this.passwordMatch = this.validate(password, rPassword);
    this.invalidForm = this.registerForm.invalid;

    if (!this.invalidForm) {
      const newUser = new UserLogin(username, password);
      this.registerService.save(newUser).subscribe(
        data => {
          this.userExists = false;
          this.userRegistered = true;
          this.registerForm.reset();
        },
        error => {
          if (error.status === 409) {
            this.userExists = true;
            this.invalidForm = true;
          }
        }
      );
    }
  }

}
