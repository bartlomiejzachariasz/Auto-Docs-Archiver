import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentNotExistingComponent } from './document-not-existing.component';

describe('DocumentNotExistingComponent', () => {
  let component: DocumentNotExistingComponent;
  let fixture: ComponentFixture<DocumentNotExistingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DocumentNotExistingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DocumentNotExistingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
