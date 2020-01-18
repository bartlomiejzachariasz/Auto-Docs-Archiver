import {Component, OnInit} from '@angular/core';
import {DocumentInfo} from '../shared/document.info';
import {Router} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {DocumentsService} from '../shared/documents.service';

@Component({
  selector: 'app-find-document',
  templateUrl: './find-document.component.html',
  styleUrls: ['./find-document.component.css']
})
export class FindDocumentComponent implements OnInit {

  selectedDocument: DocumentInfo;

  constructor(private router: Router, private http: HttpClient, private documentsService: DocumentsService) {
  }

  ngOnInit() {
  }

  selectDocument(documentInfo: DocumentInfo) {
    this.selectedDocument = documentInfo;

    this.router.navigate(['/documents', this.selectedDocument.id]);
  }

}
