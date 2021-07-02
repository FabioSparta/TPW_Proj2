import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SignupShopComponent } from './signup-shop.component';

describe('SignupShopComponent', () => {
  let component: SignupShopComponent;
  let fixture: ComponentFixture<SignupShopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SignupShopComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SignupShopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
