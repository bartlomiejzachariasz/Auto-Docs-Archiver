import {User} from './user';

export class UserService {
  private _user: User;


  get user(): User {
    return this._user;
  }

  set user(value: User) {
    this._user = value;
  }

  isLoggedIn() {
    return new Promise(
      resolve => resolve(this.user != null)
    );
  }
}
