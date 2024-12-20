import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { ToastService } from 'src/app/shared/toasts/toasts.service';
import { CommonService } from 'src/app/utilities/services/common/common.service';

@Component({
  selector: 'app-past-records',
  templateUrl: './past-records.component.html',
  styleUrls: ['./past-records.component.scss']
})
export class PastRecordsComponent implements OnInit  {

  data: any; // Full dataset
  filteredData: any[] = []; // Data after filtering
  paginatedData: any[] = []; // Current page data
  currentPage = 1; // Current page number
  pageSize = 10; // Items per page
  searchKeyword = ''; // Search input value
  public subscription: Subscription[] = [];
  constructor(public router: Router, private commonService: CommonService, public route: ActivatedRoute, private spinner: NgxSpinnerService, private toastService: ToastService) {}
  
  ngOnInit() {
    this.spinner.show();
    this.subscription[this.subscription.length] = this.commonService.pastRecordList().subscribe((data: any) => {
      if (data.status === 200 && Array.isArray(data.data)) { 
        this.data = data.data;
        this.filteredData = [...this.data]; // Initialize filteredData with all data
        this.updatePaginatedData();
        this.spinner.hide();
      }
      else
      {
        this.spinner.hide();
        this.toastService.show({ message: 'Something went wrong. Please try again.', classname: 'bg-danger text-light toastClass', delay: 1800 });

      }
      }, err => {
        this.spinner.hide();
        this.toastService.show({ message: 'Something went wrong. Please try again.', classname: 'bg-danger text-light toastClass', delay: 1800 });
      })

    }

    // Update data based on the current page
  updatePaginatedData() {
    const start = (this.currentPage - 1) * this.pageSize;
    const end = start + this.pageSize;
    this.paginatedData = this.filteredData.slice(start, end);
  }

  // Handle page change
  onPageChange(page: number) {
    this.currentPage = page;
    this.updatePaginatedData();
  }

  // Filter data based on search keyword
  filterData() {
    const keyword = this.searchKeyword.toLowerCase();
    this.filteredData = this.data.filter(item =>
      item.name.toLowerCase().includes(keyword) ||
      item.type.toLowerCase().includes(keyword) ||
      item.kyc_status.toLowerCase().includes(keyword) ||
      item.date_added.toLowerCase().includes(keyword)
    );

    // Reset to the first page and update pagination
    this.currentPage = 1;
    this.updatePaginatedData();
  }
  
    /**
   * @description navigate to detail-view
   */
    public navigateToDetailedView(thread_id:any, type:string) {
      this.router.navigate(['detail-view'], {
        queryParams: { id: thread_id, type: type }
      });
    }

      /**
   * @description navigate to home
   */
      public navigateToHome() {
        this.router.navigate(['home']);
      }
    
}
