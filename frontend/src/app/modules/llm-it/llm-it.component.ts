import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { CommonService } from 'src/app/utilities/services/common/common.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-llm-it',
  templateUrl: './llm-it.component.html',
  styleUrls: ['./llm-it.component.scss']
})
export class LlmItComponent implements OnInit {
  public subscription: Subscription[] = [];
  public baseurl = environment.baseurl;
  constructor(public router: Router, public actRoute: ActivatedRoute, private commonService: CommonService, private spinner: NgxSpinnerService) {
    
  }
  ngOnInit(): void {

  }
}
