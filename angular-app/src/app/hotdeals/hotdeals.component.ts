import { Component, OnInit } from '@angular/core';
import {Product} from "../products/products";
import {ProductsService} from "../products/products.service";

@Component({
  selector: 'app-hotdeals',
  templateUrl: './hotdeals.component.html',
  styleUrls: ['./hotdeals.component.css']
})
export class HotdealsComponent implements OnInit {
  products : Product[] | undefined;
  constructor(private productService: ProductsService) { }

  ngOnInit(): void {
    this.getHotDeals();
  }

  getHotDeals():void{
    this.productService.getHotDeals().subscribe(products=> this.products = products);
  }
}
