import {Component, Input, OnInit} from '@angular/core';
import { User } from 'src/app/_models/user';
import { UserService } from 'src/app/_services/user.service';
import {Address} from "../../_models/address";
import {FormBuilder, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-address',
  templateUrl: './address.component.html',
  styleUrls: ['./address.component.css']
})

export class AddressComponent implements OnInit {
  user: User | undefined;
  addressForm: FormGroup;
  hasAddress:boolean;
  feedback: string;

  constructor(private userService: UserService, private formBuilder: FormBuilder,) {
    this.hasAddress=false;
    this.addressForm = this.formBuilder.group({
    country: '',
    city: '',
    zip_code:'',
    street:'',
    door:'',
    floor:''
  });
    this.feedback="";
  }

  ngOnInit(): void {
    this.loadAddress()
  }

  loadAddress():void {
    this.userService.getUserInfo().subscribe(
      user=>{
        this.user=user;
        if(user.address!=null){
          this.hasAddress=true;
        this.addressForm = this.formBuilder.group({
          country: user.address?.country,
          city: user.address?.city,
          zip_code:user.address?.zip_code,
          street:user.address?.street,
          door:user.address?.door,
          floor:user.address?.floor
        });
        }
      }

    )
  }

  onSubmit() {
    if(this.hasAddress){
      let addressId = this.user?.address?.id;
      let address : Address = this.addressForm.value
      // @ts-ignore
      this.user?.address= address;
      // @ts-ignore
      this.user?.address.id = addressId;
      console.log(this.user)

      // @ts-ignore
      this.userService.updateAddress(this.user.address).subscribe(
        data => {
            this.feedback=data;
            console.log("dadde");
        },
        error => {
            this.feedback=error.text;
            console.log("here");
        });
    }
    else{
      // @ts-ignore
      this.userService.newAddress(this.addressForm.value).subscribe(
        data => {
            this.feedback=data;
        },
        error => {
            this.feedback="Failed to add new address. Beware that door and floor must be numbers";
        });
    }

  }
}
