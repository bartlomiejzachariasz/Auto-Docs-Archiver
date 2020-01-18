import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FindDocumentComponent } from './find-document.component';

describe('FindDocumentComponent', () => {
  let component: FindDocumentComponent;
  let fixture: ComponentFixture<FindDocumentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FindDocumentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FindDocumentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
