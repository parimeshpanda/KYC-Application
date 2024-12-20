import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LlmItComponent } from './llm-it.component';

describe('AstraZenecaComponent', () => {
  let component: LlmItComponent;
  let fixture: ComponentFixture<LlmItComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LlmItComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LlmItComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
