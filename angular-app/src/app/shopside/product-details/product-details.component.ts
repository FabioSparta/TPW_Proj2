import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})
export class ProductDetailsComponent implements OnInit {

  @Input() product: Product | undefined;

  constructor(private route: ActivatedRoute, private location: Location, private service: ProductsService) {}

  ngOnInit(): void {
    this.getProduct();
  }

  getProduct():void {
    // @ts-ignore
    const id = +this.route.snapshot.paramMap.get('id');
    this.service.getProduct(id).subscribe(p => this.product = p);
  }

  update():void {
    // @ts-ignore
    this.service.updateProduct(this.item.id).subscribe(() => this.goBack());
  }

  delete():void {
    // @ts-ignore
    this.service.deleteProduct(this.item.id).subscribe(() => this.goBack());
  }

  goBack(): void {
    this.location.back();
  }


}
