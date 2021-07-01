import {Component, Input, OnInit} from '@angular/core';
import {Item} from "../../_models/items";
import {ActivatedRoute} from "@angular/router";
import {ItemsService} from "../../_services/items.service";
import {Location} from "@angular/common";

@Component({
  selector: 'app-item-details',
  templateUrl: './item-details.component.html',
  styleUrls: ['./item-details.component.css']
})
export class ItemDetailsComponent implements OnInit {
  @Input() item: Item | undefined;

  constructor(private route: ActivatedRoute, private location: Location, private service: ItemsService) {}

  ngOnInit(): void {
    this.getItem();
  }

  getItem():void {
    // @ts-ignore
    const id = +this.route.snapshot.paramMap.get('id');
    this.service.getItem(id).subscribe(i => this.item = i);
  }

  update():void {
    // @ts-ignore
    this.service.updateItem(this.item.id).subscribe(() => this.goBack());
  }

  delete():void {
    // @ts-ignore
    this.service.deleteItem(this.item.id).subscribe(() => this.goBack());
  }

  goBack(): void {
    this.location.back();
  }

}
