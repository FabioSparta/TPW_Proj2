import { Component, OnInit } from '@angular/core';
import {Brand} from "../../_models/brand";
import {BrandsService} from "../../_services/brands.service";
import {OwlOptions} from "ngx-owl-carousel-o";

@Component({
  selector: 'app-brands',
  templateUrl: './brands.component.html',
  styleUrls: ['./brands.component.css']
})

export class BrandsComponent implements OnInit {

  brands : Brand[] | undefined;
  customOptions: OwlOptions  = {
    nav: false,
    navText: ["<i class='icon-angle-left'></i>","<i class='icon-angle-right'></i>"],
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

  constructor(private brandService: BrandsService) { }

  ngOnInit(): void {
    this.getBrands();
  }

  getBrands(): void{
    this.brandService.getBrands().subscribe(brands => this.brands = brands);
  }
}
