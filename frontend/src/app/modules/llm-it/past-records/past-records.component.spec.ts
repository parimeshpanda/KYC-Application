import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PastRecordsComponent } from './past-records.component';

describe('PastRecordsComponent', () => {
  let component: PastRecordsComponent;
  let fixture: ComponentFixture<PastRecordsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PastRecordsComponent]
    });
    fixture = TestBed.createComponent(PastRecordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
