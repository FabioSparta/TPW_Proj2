import { Component, OnInit } from '@angular/core';
import {Order} from "../../_models/order";
import {OrderService} from "../../_services/order.service";

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: Order[] | undefined;
  constructor(private orderService: OrderService) { }

  ngOnInit(): void {
    this.getOrders();
  }

  getOrders(): void{
    this.orderService.getOrders().subscribe(orders=>this.orders = orders)
  }

}
