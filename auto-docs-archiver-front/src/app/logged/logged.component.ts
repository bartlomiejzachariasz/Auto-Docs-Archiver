import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {User} from '../shared/user';
import {TokenStorage} from '../auth/token.storage';
import {Router} from '@angular/router';
import {UserService} from '../shared/user.service';

@Component({
  selector: 'app-logged',
  templateUrl: './logged.component.html',
  styleUrls: ['./logged.component.css']
})
export class LoggedComponent implements OnInit {
  private user: User;

  userReady = false;
  @Output() private logOutEvent = new EventEmitter();

  constructor(private tokenStorage: TokenStorage, private router: Router,
              private userService: UserService) {
  }

  ngOnInit() {
    this.userReady = false;
    this.user = new User(this.tokenStorage.getUsername());
    this.userService.user = this.user;
  }

  logoutUser() {
    this.tokenStorage.logout();
    window.location.reload();

  }
}
