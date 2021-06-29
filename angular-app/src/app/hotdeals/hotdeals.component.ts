import { Component, OnInit } from '@angular/core';
import {Product} from "../_models/products";
import {ProductsService} from "../_services/products.service";

@Component({
  selector: 'app-hotdeals',
  templateUrl: './hotdeals.component.html',
  styleUrls: ['./hotdeals.component.css']
})
export class HotdealsComponent implements OnInit {

  products : Product[] | undefined;
  abc : string
  constructor(private productService: ProductsService) {
    this.abc= "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  }

  ngOnInit(): void {
    this.getHotDeals();
  }

  getHotDeals():void{
    this.productService.getHotDeals().subscribe(products=> {
      this.products = products;
    });
  }
}
