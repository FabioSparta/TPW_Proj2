import { Component, OnInit } from '@angular/core';
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";
import {OwlOptions} from "ngx-owl-carousel-o";

@Component({
  selector: 'app-hotdeals',
  templateUrl: './hotdeals.component.html',
  styleUrls: ['./hotdeals.component.css']
})

export class HotdealsComponent implements OnInit {

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

  constructor(private productService: ProductsService) {}

  ngOnInit(): void {
    this.getHotDeals();
  }


  getHotDeals():void{
    this.productService.getHotDeals().subscribe(products=> {
      this.products = products;
    });
  }
}
