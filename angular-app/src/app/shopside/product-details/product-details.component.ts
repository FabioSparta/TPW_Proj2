import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Product} from "../../_models/products";
import {ProductsService} from "../../_services/products.service";
import {CategoriesService} from "../../_services/categories.service";
import {BrandsService} from "../../_services/brands.service";
import {Category} from "../../_models/category";
import {Brand} from "../../_models/brand";

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

  constructor(private route: ActivatedRoute, private location: Location, private prodService: ProductsService,private catService: CategoriesService, private brandService: BrandsService) {}

  ngOnInit(): void {
    this.getProduct();
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
    this.prodService.updateProduct(this.item.id).subscribe(() => this.goBack(), (err) => console.log(err));
  }

  delete():void {
    // @ts-ignore
    this.prodService.deleteProduct(this.item.id).subscribe(() => this.goBack());
  }

  goBack(): void {
    this.location.back();
  }

}
