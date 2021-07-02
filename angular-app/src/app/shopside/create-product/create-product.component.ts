import {Component, Input, OnInit} from '@angular/core';
import { FormBuilder } from '@angular/forms';
import {Category} from "../../_models/category";
import {Brand} from "../../_models/brand";
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {ProductsService} from "../../_services/products.service";
import {CategoriesService} from "../../_services/categories.service";
import {BrandsService} from "../../_services/brands.service";
import {Product} from "../../_models/products";

@Component({
  selector: 'app-create-product',
  templateUrl: './create-product.component.html',
  styleUrls: ['./create-product.component.css']
})

export class CreateProductComponent implements OnInit {

  categories : Category[] | undefined;
  brands : Brand[] | undefined;
  selectedFile?: File

  createProdForm = this.formBuilder.group({
    reference:'',
    name: '',
    details: '',
    warehouse: '',
    price: 0,
    new_category:'',
    new_brand:'',
    category:'',
    brand:'',
  });


  constructor(private route: ActivatedRoute, private location: Location, private prodService: ProductsService,private catService: CategoriesService, private brandService: BrandsService,private formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.createProdForm = this.formBuilder.group({
    reference:'',
    name: '',
    details: '',
    warehouse: '',
    price: 0,
    new_category:'',
    new_brand:'',
    category:'',
    brand:'',
  });
    this.createProdForm.controls['new_category'].disable()
    this.createProdForm.controls['new_brand'].disable()
    this.getCategories();
    this.getBrands();
  }

  onFileChanged(event: Event) {
    // @ts-ignore
    this.selectedFile = event.target.files[0]
  }

  getCategories():void {
    this.catService.getCategories().subscribe(cat => this.categories = cat);
  }

  getBrands(): void {
    this.brandService.getBrands().subscribe(brands => this.brands = brands);
  }

  onSubmit(): void {
    // @ts-ignore
    let new_cat = this.createProdForm.controls['new_category'].value
    let new_brand = this.createProdForm.controls['new_brand'].value
    let price = this.createProdForm.controls['price'].value
    let reference = this.createProdForm.controls['reference'].value
    let details = this.createProdForm.controls['details'].value
    let warehouse = this.createProdForm.controls['warehouse'].value
    let name = this.createProdForm.controls['name'].value
    let brand = this.createProdForm.controls['brand'].value
    let category = this.createProdForm.controls['category'].value

      // @ts-ignore
    this.prodService.createProduct(new Product(reference,name,warehouse,details,category,brand),new_cat, new_brand, price).subscribe(() => this.goBack(), (err) => console.log(err));
    this.createProdForm.reset();
  }

  goBack(): void {
    location.href = '/products';
  }

  selectChange(type: string): void{
    if (type == 'category'){
      let cat = this.createProdForm.controls['category'];
      let new_cat = this.createProdForm.controls['new_category'];
      if (cat.value.name == 'Other')
        new_cat.enable();
      else
        new_cat.disable();
    }

    if (type == 'brand'){
      let b = this.createProdForm.controls['brand'];
      let new_b = this.createProdForm.controls['new_brand'];

      if (b.value.name == 'Other')
        new_b.enable();
      else
        new_b.disable();
    }
  }

}
