
export class Category{
    id: number;
    name: string;
    totDevices:number;
    image?:string;

  constructor(id:number ,name:string, totDevs:number = 0) {
    this.id = id;
    this.name = name;
    this.totDevices = totDevs;
  }
}
