import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {ProductsService} from "../../_services/products.service";
import {FormBuilder, Validators} from "@angular/forms";
import {Product} from "../../_models/products";
import {ItemsService} from "../../_services/items.service";
import {Item} from "../../_models/items";
import {ShopsService} from "../../_services/shops.service";

@Component({
  selector: 'app-create-item',
  templateUrl: './create-item.component.html',
  styleUrls: ['./create-item.component.css']
})
export class CreateItemComponent implements OnInit {
  products? : Product[];
  selectedProd: number | undefined;

  createItemForm = this.formBuilder.group({
    price: 0,
    stock: 0,
    prod: ['', Validators.required],
  });


  constructor(private route: ActivatedRoute, private location: Location,private itemsService: ItemsService,private shopsService :ShopsService, private prodService: ProductsService,private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.getProds();
  }

  getProds():void {
    this.prodService.getProducts().subscribe(p => this.products = p);
  }


  onSubmit(): void {
    if (this.selectedProd) {
   // @ts-ignore
      let prod = this.products[this.selectedProd]

      // @ts-ignore
      this.itemsService.createItem(new Item(this.createItemForm.value.price, this.createItemForm.value.stock, prod)).subscribe(() => this.goBack(), (err) => console.log(err));
      this.createItemForm.reset();
    }
    else
      console.log('Choose a product please')
  }

  selectChange(): void{
    this.selectedProd = this.createItemForm.get('prod')?.value;
  }

  goBack(): void {
    this.location.back();
  }

}
