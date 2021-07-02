import { Component, OnInit } from '@angular/core';
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.css']
})

export class ProductsComponent implements OnInit {

  products : Product[] | undefined;
  loaded: boolean;

  constructor(private productsService: ProductsService) { this.loaded=false; }

  ngOnInit(): void {
    this.getProducts();
  }

  getProducts():void{
    this.productsService.getShopProducts().subscribe(prods => {this.products = prods; this.loaded=true;});
  }


}
