import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../_services/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isShop: string;
  isAuthenticated : boolean
  username: string;

  constructor(private authService: AuthService,private router: Router,) {
    this.isShop="false";
    this.isAuthenticated=false;
    this.username= "User"
  }

  ngOnInit(): void {
    let username = this.authService.getUsername()
    if(username != "") this.username = username;

    let isShop= this.authService.isShop();
    if(isShop!=null) this.isShop= <string>isShop;

    this.isAuthenticated = this.authService.isAuthenticated()
  }

  logout():void{
    this.authService.logout();
    window.location.reload();
  }


}
