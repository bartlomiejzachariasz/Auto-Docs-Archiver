import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentElementComponent } from './document-element.component';

describe('DocumentElementComponent', () => {
  let component: DocumentElementComponent;
  let fixture: ComponentFixture<DocumentElementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocumentElementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocumentElementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
