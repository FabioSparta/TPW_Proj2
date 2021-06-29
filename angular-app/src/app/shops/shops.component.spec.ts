import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShopsComponent } from '../_models/shops.component';

describe('ShopsComponent', () => {
  let component: ShopsComponent;
  let fixture: ComponentFixture<ShopsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShopsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShopsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
