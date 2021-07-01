import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {User} from "../../_models/user";
import {HttpErrorResponse} from '@angular/common/http';
import {Router} from "@angular/router";
import {AlertService} from "../../_services/alert.service";
import {AuthService} from "../../_services/auth.service";
import {first} from "rxjs/operators";

@Component({
  selector: 'app-sign-in-up',
  templateUrl: './sign-in-up.component.html',
  styleUrls: ['./sign-in-up.component.css']
})
export class SignInUpComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  submitted = false;

  constructor( private formBuilder: FormBuilder,
               private router: Router,
               private authService: AuthService,
               private alertService: AlertService ) {
    //Login Form
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required, Validators.maxLength(20)],
      password: ['', [Validators.required, Validators.maxLength(25)]]}
    );
  }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  // Getter for form fields
  get f(): any { return this.loginForm.controls; }


  onLogin(): void {
    this.submitted = true;

    // reset alerts on submit
    this.alertService.clear();

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
          this.loading = false;
          this.router.navigate(['/']);
        },
        error => {
          this.alertService.error(error);
          this.loading = false;
        });
  }

}
