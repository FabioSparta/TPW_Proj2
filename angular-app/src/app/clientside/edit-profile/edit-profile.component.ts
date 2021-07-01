import { Component, OnInit } from '@angular/core';
import {User} from "../../_models/user";
import {FormBuilder, FormGroup} from "@angular/forms";
import {UserService} from "../../_services/user.service";
@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})

export class EditProfileComponent implements OnInit {
  user: User | undefined;
  profileForm: FormGroup;
  feedback: string;

  constructor(private userService: UserService, private formBuilder: FormBuilder,) {
    this.profileForm = this.formBuilder.group({
      email: '',
      username: '',
      first_name:'',
      last_name:'',
      gender:'',
      phone_number:'',
      age: '',
    });
    this.feedback="";
  }

  ngOnInit(): void {
    this.loadProfile()
  }

  loadProfile():void {
    this.userService.getUserInfo().subscribe(
      user=>{
        console.log("this is the user");
        console.log(user);
        this.profileForm = this.formBuilder.group({
          email: user.django_user.email,
          username: user.django_user.username,
          first_name:user.django_user.first_name,
          last_name:user.django_user.last_name,
          gender:user.gender,
          phone_number:user.phone_number,
          age: user.age
        });
      }
    )
  }

  onSubmit() {
    console.log("form values")
    console.log(this.profileForm.value)
    // @ts-ignore
    this.userService.updateUser(this.profileForm.value).subscribe(
      data => {
        this.feedback=data;
      },
      error => {
        this.feedback="Failed to update account";
      });
  }


}
