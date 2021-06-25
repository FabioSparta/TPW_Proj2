import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewarrivalsComponent } from './newarrivals.component';

describe('NewarrivalsComponent', () => {
  let component: NewarrivalsComponent;
  let fixture: ComponentFixture<NewarrivalsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewarrivalsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewarrivalsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
