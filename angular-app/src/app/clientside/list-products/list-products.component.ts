import {Component, Input, OnInit} from '@angular/core';
import {ProductsService} from "../../_services/products.service";
import {Product} from "../../_models/products";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-list-products',
  templateUrl: './list-products.component.html',
  styleUrls: ['./list-products.component.css']
})
export class ListProductsComponent implements OnInit {
  products : Product[] | undefined;
  loaded:boolean;
  constructor(private productService: ProductsService, private route: ActivatedRoute) { this.loaded=false;}

  ngOnInit(): void {
    this.searchProducts();
  }

  searchProducts():void{
    if(this.route.snapshot.paramMap.has("key") && this.route.snapshot.paramMap.has("cat")){
      let key = this.route.snapshot.paramMap.get("key");
      let cat = this.route.snapshot.paramMap.get("cat");

      if(key==null){
        key="";
      }
      if(cat==null){
        cat="";
      }

      this.productService.searchProductsByKeyAndCat(key,cat).subscribe(products=> {
        this.products = products;
        this.loaded=true;
      });
    }

    if(!this.route.snapshot.paramMap.has("key") && !this.route.snapshot.paramMap.has("cat")){
      this.productService.searchAllProducts().subscribe(products=> {
        this.products = products;
        this.loaded=true;
      });
    }

    if(!this.route.snapshot.paramMap.has("key")){
      let cat = this.route.snapshot.paramMap.get("cat");

      if(cat==null){
        cat="";
      }

      this.productService.searchProductsByCat(cat).subscribe(products=> {
        this.products = products;
        this.loaded=true;
      });
    }


  }
}
