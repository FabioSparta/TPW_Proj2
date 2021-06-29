import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShopsCarouselComponent } from './shops-carousel.component';

describe('ShopsCarouselComponent', () => {
  let component: ShopsCarouselComponent;
  let fixture: ComponentFixture<ShopsCarouselComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShopsCarouselComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShopsCarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
