import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../_services/auth.service";

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})

export class UserProfileComponent implements OnInit {

  username: string;

  constructor(private authService : AuthService) {

    this.username="";
  }

  ngOnInit(): void {}


  getUsername(): void{
    this.username=this.authService.getUsername();
  }

  logout():void{
    this.authService.logout();
    window.location.reload();
  }

}
