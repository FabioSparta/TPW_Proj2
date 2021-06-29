import { Component, OnInit } from '@angular/core';
import {Brand} from "./brand";
import {BrandsService} from "../../_services/brands.service";

@Component({
  selector: 'app-brands',
  templateUrl: './brands.component.html',
  styleUrls: ['./brands.component.css']
})
export class BrandsComponent implements OnInit {
  brands : Brand[] | undefined;
  constructor(private brandService: BrandsService) { }

  ngOnInit(): void {
    this.getBrands();
  }

  getBrands(): void{
    this.brandService.getBrands().subscribe(brands => this.brands = brands);
  }
}
