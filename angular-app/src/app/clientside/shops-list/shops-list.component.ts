import { Component, OnInit } from '@angular/core';
import {Shop} from "../../_models/shop";
import {ShopsService} from "../../_services/shops.service";

@Component({
  selector: 'app-shops-list',
  templateUrl: './shops-list.component.html',
  styleUrls: ['./shops-list.component.css']
})

export class ShopsListComponent implements OnInit {
  shops : Shop[] | undefined;
  loaded: boolean;

  constructor(private shopService : ShopsService) {
    this.loaded=false;
  }

  ngOnInit(): void {
    this.getShops();
  }

  getShops(): void{
    this.shopService.getShops().subscribe(shops =>{
      this.shops=shops
      this.loaded=true;
    });
  }

}
