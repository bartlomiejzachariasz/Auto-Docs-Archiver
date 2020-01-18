import {Component} from '@angular/core';
import {Router} from '@angular/router';
import {TokenStorage} from './auth/token.storage';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private router: Router, private tokenStorage: TokenStorage) {
  }

  logUserOut() {
    this.router.navigate(['/']);
  }
}
