import { Component, OnInit } from '@angular/core';
import {OwlOptions} from "ngx-owl-carousel-o";
import {Shop} from "../../_models/shop";
import {ShopsService} from "../../_services/shops.service";

@Component({
  selector: 'app-shops-carousel',
  templateUrl: './shops-carousel.component.html',
  styleUrls: ['./shops-carousel.component.css']
})

export class ShopsCarouselComponent implements OnInit {
  shops : Shop[] | undefined
  customOptions: OwlOptions  = {
    nav: false,
    navText: ["<div class='prev-slide'></div>","<div class='next-slide'></div>"],
    items: 5,
    loop: true,
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

  constructor(private shopService : ShopsService) { }

  ngOnInit(): void {
    this.getShops();
  }

  getShops(): void{
    this.shopService.getShops().subscribe(shops => this.shops=shops);
  }

}
