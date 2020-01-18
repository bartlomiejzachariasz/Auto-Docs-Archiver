import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DocumentInfo} from '../../shared/document.info';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-document-element',
  templateUrl: './document-element.component.html',
  styleUrls: ['./document-element.component.css']
})
export class DocumentElementComponent implements OnInit {
  @Input() documentInfo: DocumentInfo;
  private API = 'http://localhost:8000/documents/';

  @Output() chosenDocumentEvent = new EventEmitter<DocumentInfo>();


  constructor(private http: HttpClient) {
  }

  ngOnInit() {
  }

  onSelect() {
    const documentAPI = this.API + this.documentInfo.id;
    this.http.get<DocumentInfo>(documentAPI).subscribe(
      data => {
        this.documentInfo = data;
        this.chosenDocumentEvent.emit(this.documentInfo);
      },
      error => {
        console.log(error);
      }
    );
  }

}
