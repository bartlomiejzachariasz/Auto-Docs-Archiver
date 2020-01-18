import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {DocumentsService} from '../shared/documents.service';
import {DocumentInfo} from '../shared/document.info';

@Component({
  selector: 'app-documents-list',
  templateUrl: './documents-list.component.html',
  styleUrls: ['./documents-list.component.css']
})
export class DocumentsListComponent implements OnInit {
  public file: any;
  @Output() chosenDocumentEvent = new EventEmitter<DocumentInfo>();
  @Input() searchBox: string;

  documentsSnapshot: any[];

  private API = 'http://localhost:8000/documents';

  constructor(private http: HttpClient, private documentsService: DocumentsService) {
  }

  ngOnInit() {
    this.documentsService.updateDocuments();
  }

  uploadFile(event: any) {
    const formData: FormData = new FormData();
    formData.append('file', event.target.files[0]);
    this.http.post(this.API, formData).subscribe(
      data => console.log(data));
  }

  chosenDocument(documentInfo: DocumentInfo) {
    this.chosenDocumentEvent.emit(documentInfo);
  }

  public search() {
    this.documentsSnapshot = Object.assign([], this.documentsService.documentsList);

    this.documentsService.documentsList = this.documentsService.documentsList.filter(
      document => document.category.toLowerCase().includes(this.searchBox.toLowerCase())
    );
  }
  public resetFilters() {
    this.documentsService.documentsList = Object.assign([], this.documentsSnapshot);
    this.searchBox = '';
  }
}
