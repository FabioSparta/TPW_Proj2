import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";
import {CategoriesService} from "../../_services/categories.service";
import {BrandsService} from "../../_services/brands.service";
import {Category} from "../../_models/category";
import {Brand} from "../../_models/brand";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.css']
})

export class ProductDetailsComponent implements OnInit {

  @Input() product: Product | undefined;
  categories : Category[] | undefined;
  brands : Brand[] | undefined;
  selectedFile?: File

  createProdForm = this.formBuilder.group({
    cat:'',
    brand:'',
    new_category:'',
    new_brand:'',
  });

  constructor(private route: ActivatedRoute, private location: Location, private prodService: ProductsService,private catService: CategoriesService, private brandService: BrandsService,private formBuilder: FormBuilder) {}

  ngOnInit(): void {

    this.getProduct();
    this.createProdForm.controls['new_category'].disable()
    this.createProdForm.controls['new_brand'].disable()
    this.getCategories();
    this.getBrands();
  }

  onFileChanged(event: Event) {
    // @ts-ignore
    this.selectedFile = event.target.files[0]
  }

  getProduct():void {
    // @ts-ignore
    const id = +this.route.snapshot.paramMap.get('id');
    this.prodService.getProduct(id).subscribe(p => this.product = p);
  }

  getCategories():void {
    this.catService.getCategories().subscribe(cat => this.categories = cat);
  }

  getBrands(): void {
    this.brandService.getBrands().subscribe(brands => this.brands = brands);
  }

  update():void {
    // @ts-ignore
    this.prodService.updateProduct(this.product).subscribe(() => this.goBack(), (err) => console.log(err));
  }

  delete():void {
    // @ts-ignore
    this.prodService.deleteProduct(this.product.id).subscribe(() => this.goBack());
  }

  goBack(): void {
    // @ts-ignore
    document.getElementById("closeBtn").click();
    this.location.back();
  }

  selectChange(type: string): void{
    if (type == 'category'){
      let cat = this.createProdForm.controls['cat'];
      let new_cat = this.createProdForm.controls['new_category'];
      if (cat.value == 'Other')
        new_cat.enable();
      else
        new_cat.disable();
    }

    if (type == 'brand'){
      let b = this.createProdForm.controls['brand'];
      let new_b = this.createProdForm.controls['new_brand'];

      if (b.value == 'Other')
        new_b.enable();
      else
        new_b.disable();
    }
  }
}
