import { Component } from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title = 'Tech Sekai';
  showNavabar = true;

  constructor(private router: Router) {}

  ngOnInit() {

    // Keep track of the current href
    this.router.events.subscribe((e) => {

      if (e instanceof NavigationEnd) {
        // No Navbar when in /login or /signUp
        this.showNavabar = !(e.url === "/login" || e.url === "/signup" || e.url=== "/signup/shop");
      }
    });
  }
}
