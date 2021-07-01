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
  @Input() item?: Item;
  feedback = ""

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
    this.service.updateItem(this.item).subscribe(() => this.goBack(),
      (err) => {
        // @ts-ignore
        for (const [key, value] of Object.entries(err.error)) {
          // @ts-ignore
          for (const [k, val] of Object.entries(value)) {
            console.log(key + " : " + val);
            // @ts-ignore
            this.feedback += ("\n".concat(key.concat(" : ").concat(val)).concat("\n")).toString();
          }
        }
        ;console.log(err)
      });
  }

  delete():void {
    // @ts-ignore
    this.service.deleteItem(this.item.id).subscribe(() => this.goBack(),
      (err) => {
        // @ts-ignore
            this.feedback += err.error;
            // @ts-ignore
            document.getElementById("closeBtn").click();
        }
    );
  }

  goBack(): void {
    // @ts-ignore
    document.getElementById("closeBtn").click();
    location.href = '/items';
  }

}
