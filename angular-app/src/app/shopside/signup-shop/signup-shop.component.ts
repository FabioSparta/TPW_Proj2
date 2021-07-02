import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {AuthService} from "../../_services/auth.service";
import {first} from "rxjs/operators";

@Component({
  selector: 'app-signup-shop',
  templateUrl: './signup-shop.component.html',
  styleUrls: ['./signup-shop.component.css']
})
export class SignupShopComponent implements OnInit {
  registerForm: FormGroup;
  loading = false;
  submitted = false;
  registerError: string;

  constructor( private formBuilder: FormBuilder,
               private router: Router,
               private authService: AuthService,) {

    this.registerError = "";
    //Register Form
    this.registerForm = this.formBuilder.group({
      email:    ['', Validators.required],
      username: ['', [Validators.required, Validators.maxLength(20)]],
      password: ['', [Validators.required, Validators.maxLength(25)]],
      shop_name: ['', [Validators.required, Validators.maxLength(25)]],
      shop_number: ['', [Validators.required, Validators.maxLength(25)]]
    });
  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      email:    ['', Validators.required],
      username: ['', [Validators.required, Validators.maxLength(20)]],
      password: ['', [Validators.required, Validators.maxLength(25)]],
      shop_name: ['', [Validators.required, Validators.maxLength(25)]],
      shop_number: ['', [Validators.required, Validators.maxLength(25)]]
    });

    this.registerForm.valueChanges.subscribe(formValue => {  });

  }

  // Getter for form fields
  get f(): any { return this.registerForm.controls; }

  onSignUp(): void {
    this.submitted = true;
    // stop here if form is invalid
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;
    this.authService.signUpShop(this.registerForm.value)
      .pipe(first())
      .subscribe(
        data => {
          this.router.navigate(['/login']);
        },
        error => {
          this.registerError = error.text;
          this.loading = false;
        });
  }

}
