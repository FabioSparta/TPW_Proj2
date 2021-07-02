import { Component, OnInit } from '@angular/core';
import {Item} from "../../_models/items";
import {ItemsService} from "../../_services/items.service";

@Component({
  selector: 'app-items',
  templateUrl: './items.component.html',
  styleUrls: ['./items.component.css']
})
export class ItemsComponent implements OnInit {

  items : Item[] | undefined;
  loaded:boolean;

  constructor(private itemsService: ItemsService) {this.loaded=false; }

  ngOnInit(): void {
    this.getItems();
  }

  getItems():void{
    this.itemsService.getItems().subscribe(items => {this.items = items; this.loaded=true;});
  }


}
