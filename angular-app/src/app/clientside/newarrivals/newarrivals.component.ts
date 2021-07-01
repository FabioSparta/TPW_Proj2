import { Component, OnInit } from '@angular/core';
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";
import {OwlOptions} from "ngx-owl-carousel-o";

@Component({
  selector: 'app-newarrivals',
  templateUrl: './newarrivals.component.html',
  styleUrls: ['./newarrivals.component.css']
})
export class NewarrivalsComponent implements OnInit {
  products : Product[] | undefined;

  customOptions: OwlOptions  = {
    nav: true,
    navText: ["<div class='prev-slide'></div>","<div class='next-slide'></div>"],
    items: 5,
    loop: false,
    center: false,
    margin: 20,
    lazyLoad: true,
    dots: true,
    autoplay:true,
    autoplayTimeout:1900,
    responsive: {
      "0": {
        "items":2
      },
      "480": {
        "items":2
      },
      "768": {
        "items":3
      },
      "992": {
        "items":4
      },
      "1280": {
        "items":5,
        "nav": true
      }
    }
  }

  constructor(private productService: ProductsService) { }

  ngOnInit(): void {
    this.getNewArrivals();
  }

  getNewArrivals():void{
    this.productService.getNewArrivals().subscribe(products=> this.products = products);
  }

}
