import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {User} from "../user-profile/user";
import {HttpErrorResponse} from '@angular/common/http';
import {Router} from "@angular/router";

@Component({
  selector: 'app-sign-in-up',
  templateUrl: './sign-in-up.component.html',
  styleUrls: ['./sign-in-up.component.css']
})
export class SignInUpComponent implements OnInit {
  loginError = false;
  loginForm: FormGroup;
  loading = false;
  submitted = false;

  constructor( private formBuilder: FormBuilder, private router: Router) {
    //Login Form
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required, Validators.maxLength(20)],
      password: ['', [Validators.required, Validators.maxLength(25)]]}
    );
  }

  ngOnInit(): void {}

  // Getter for form fields
  get f(): any { return this.loginForm.controls; }


  onLogin(): void {
    this.submitted = true;
    if (this.loginForm.invalid) {
      return;
    }
    this.loading = true;
   // TODO: call authentication service here
  }

}
