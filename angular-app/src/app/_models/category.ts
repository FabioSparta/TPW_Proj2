
export class Category{
    id: number;
    name: string;
    totDevices:number;
    image?:string;

  constructor(name:string, totDevs:number = 0, id:number) {
    this.id = id;
    this.name = name;
    this.totDevices = totDevs;
  }
}
