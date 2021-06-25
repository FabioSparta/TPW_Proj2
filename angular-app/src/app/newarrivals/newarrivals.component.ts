import { Component, OnInit } from '@angular/core';
import {Product} from "../products/products";
import {ProductsService} from "../products/products.service";

@Component({
  selector: 'app-newarrivals',
  templateUrl: './newarrivals.component.html',
  styleUrls: ['./newarrivals.component.css']
})
export class NewarrivalsComponent implements OnInit {
  products : Product[] | undefined;
  constructor(private productService: ProductsService) { }

  ngOnInit(): void {
    this.getNewArrivals();
  }

  getNewArrivals():void{
    this.productService.getNewArrivals().subscribe(products=> this.products = products);
  }

}
