import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {User} from "../../_models/user";
import {HttpErrorResponse} from '@angular/common/http';
import {Router} from "@angular/router";
import {AuthService} from "../../_services/auth.service";
import {first} from "rxjs/operators";

@Component({
  selector: 'app-sign-in-up',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})

export class SignInComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  submitted = false;
  loginError: boolean;

  constructor( private formBuilder: FormBuilder,
               private router: Router,
               private authService: AuthService,
               ) {
    //Login Form
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required, Validators.maxLength(20)],
      password: ['', [Validators.required, Validators.maxLength(25)]]}
    );
    this.loginError = false;
    this.loginForm.valueChanges.subscribe(formValue => {  });
  }

  ngOnInit(): void {}

  // Getter for form fields
  get f(): any { return this.loginForm.controls; }


  onLogin(): void {
    this.submitted = true;

    // stop here if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    this.authService.signIn(this.f.username.value, this.f.password.value)
      .pipe(first())
      .subscribe(
        data => {
          localStorage.setItem('userToken', data.token); // Save Token
          this.saveRole()
        },
        error => {
          this.loginError=true;
          this.loading = false;
        });
  }

  saveRole(): void{
    this.authService.getRole().subscribe(
      data=>{
      localStorage.setItem('isShop',data.isShop);
      localStorage.setItem('userId',data.userId);
      localStorage.setItem('username',data.username);
      localStorage.setItem('shopId',data.shopId);
        this.router.navigate(['/']);
    })
  }

}
