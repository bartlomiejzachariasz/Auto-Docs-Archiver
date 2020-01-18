import {Component, Input, OnInit} from '@angular/core';
import {DocumentsService} from '../shared/documents.service';
import {HttpClient} from '@angular/common/http';
import {ActivatedRoute, Router} from '@angular/router';
import {DocumentInfo} from '../shared/document.info';

@Component({
  selector: 'app-document-details',
  templateUrl: './document-details.component.html',
  styleUrls: ['./document-details.component.css']
})
export class DocumentDetailsComponent implements OnInit {
  public selectedDocument: DocumentInfo;
  private API = 'http://localhost:8000/documents/';

  constructor(private documentsService: DocumentsService, private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  }

  ngOnInit() {
    this.http.get<DocumentInfo>(this.API + this.route.snapshot.params['id']).subscribe(
      data => {
        this.selectedDocument = data;
      },
      error => {
        console.log(error);
      }
    );
  }

  updateDate() {
    this.http.put(this.API + this.route.snapshot.params['id'], {'date': this.selectedDocument.date});
  }


}
