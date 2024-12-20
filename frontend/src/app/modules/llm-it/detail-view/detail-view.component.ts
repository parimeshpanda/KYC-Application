import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { CommonService } from 'src/app/utilities/services/common/common.service';
@Component({
  selector: 'app-detail-view',
  templateUrl: './detail-view.component.html',
  styleUrls: ['./detail-view.component.scss']
})
export class DetailViewComponent implements OnInit, OnDestroy {
  public details:any;
  threadId!: string;
  kyc_type: string;
  threadData:any;
  threadDetails: any;
  public subscription: Subscription[] = [];
  constructor(private commonService: CommonService, public route: ActivatedRoute, public router: Router, private spinner: NgxSpinnerService) {

  }
  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.threadId = params['id'];
      this.kyc_type = params['type']
      if (this.threadId) {
        this.fetchThreadDetails(this.threadId);
      }
    });

   
   }
  
   public fetchThreadDetails(threadId: any) {
    this.spinner.show();
    this.subscription[this.subscription.length] = this.commonService.pastRecords(threadId).subscribe((data: any) => {
      if (data.status === 200 && Array.isArray(data.data)) { 
        this.threadData = data.data;
        this.threadDetails = data.data.filter((item: any) => item.conversation_type !== '');
        this.spinner.hide();
      }
      
    }, err => {
      this.spinner.hide();
      console.error('Error fetching thread details:', err);
    })
    
}

    /**
   * @description navigate to explaination
   */
    public navgateToExplanation(thread_id:any) {
      this.router.navigate(['explanation'], {
        queryParams: { id: thread_id, type: this.kyc_type}
      });
    }

      /**
   * @description navigate to past-records
   */
      public navigateToPastRecords() {
        this.router.navigate(['past-records']);
      }
  
    ngOnDestroy(): void {
      this.subscription.forEach((x: any) => {
        x.unsubscribe()
      })
    }
}
