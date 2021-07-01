import {Component, Input, OnInit} from '@angular/core';
import {Shop} from "../../_models/shop";
import {ActivatedRoute} from "@angular/router";
import {ShopsService} from "../../_services/shops.service";
import {Location} from "@angular/common";

@Component({
  selector: 'app-shop-details',
  templateUrl: './shop-details.component.html',
  styleUrls: ['./shop-details.component.css']
})

export class ShopDetailsComponent implements OnInit {
  @Input() shop: Shop | undefined ;

  constructor(private route:ActivatedRoute,
              private location:Location,
              private shopService : ShopsService ) { }

  ngOnInit(): void {
    this.getShopDetails();
  }

  getShopDetails():void {
    // @ts-ignore
    const id = +this.route.snapshot.paramMap.get('id');
    this.shopService.getShopDetails(id).subscribe(shop => {
      this.shop=shop;
      console.log(shop);
    })
  }

}
