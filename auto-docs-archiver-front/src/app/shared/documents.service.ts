import {DocumentInfo} from './document.info';
import {HttpClient} from '@angular/common/http';
import {Inject, Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DocumentsService {
  documentsList: DocumentInfo[];
  private documentsAPI = 'http://localhost:8000/documents';

  constructor(private http: HttpClient) {
  }

  updateDocuments() {
    this.http.get<DocumentInfo[]>(this.documentsAPI).subscribe(
      data => {
        console.log(data);
        this.documentsList = data;
      }
    );
  }

  getDocuments() {
    this.http.get<DocumentInfo[]>(this.documentsAPI);
  }
}
