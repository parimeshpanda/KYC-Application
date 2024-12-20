import { CommonService } from 'src/app/utilities/services/common/common.service';
import { Component, Inject, OnDestroy, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal, NgbPopover } from '@ng-bootstrap/ng-bootstrap';

import { Subscription } from 'rxjs';
import { AuthService } from 'src/app/utilities/services/common/authentication.service';

import { okta } from '../config/app-config';
import { environment } from 'src/environments/environment';
import OktaAuth from '@okta/okta-auth-js';
import { OKTA_AUTH } from '@okta/okta-angular';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastService } from '../toasts/toasts.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  @ViewChild('modalTemplate') modalTemplate!: TemplateRef<any>;
  public baseurl: string = environment.baseurl = '';
  public userDetails: any = null;
  @ViewChild('ngbPopover') public ngbPopover!: NgbPopover;
  private sub: Subscription[] = [];
  public isAuthenticated: boolean = false;
  threadDetails:any;
  isPopupOpen: boolean = false;
  constructor(private modalService: NgbModal, public router: Router,
  private auth: AuthService,
  private route: ActivatedRoute,
  @Inject(OKTA_AUTH) private oktaAuth: OktaAuth,
    private commonService: CommonService, private toastService: ToastService, private spinner: NgxSpinnerService) { }

    formattedTime$ = this.commonService.formattedTime$; // Subscribe to timer updates
  ngOnInit(): void {
    this.sub[this.sub.length] = this.auth.getUserInfo().subscribe((data: any) => {
      if (data) {
        this.userDetails = data;
      }
    })
    
  }

  /**
   * @description navigate to home
   */
  public navigateToHome() {

    if (this.router.url !== '/' && this.router.url !== '/home') {
      this.router.navigate(['/home']);
    }
  }

   /**
   * @description navigate to past-records
   */
   public navigateToPastRecords() {
    this.router.navigate(['past-records']);
  }



  /**
   * @description logout okta
   */
  public async logout(): Promise<void> {
    if (okta) {
      await this.oktaAuth.signOut({
        postLogoutRedirectUri: environment.postLogoutRedirectUri
      })
      localStorage.clear();
    }
  }

  /**
   * @description close filter popup
   * @param p1 
   */
  public closePop(p1?: any) {
    p1 ? p1.close() : '';
  }

  /**
   * @description open filter popup
   * @param p1 
   */
  public openPop(p1?: any) {
    p1.open();
  }

  public confirmPopUp() {
    this.isPopupOpen = true; 
    const modalRef = this.modalService.open(this.modalTemplate, { windowClass: 'newChatPopup',size: 'md', centered: true,   backdrop: 'static', keyboard: false, });
    modalRef.result.finally(() => {
      this.isPopupOpen = false; // Reset flag when popup closes
    });
  }

  

  public agree(){
    this.spinner.show();
    this.sub[this.sub.length] = this.commonService.startChat().subscribe((data: any) => {
    this.spinner.hide();
    if (data.status == 200)
      this.threadDetails = data;
    localStorage.removeItem('threadData');
    localStorage.setItem('threadData', JSON.stringify(data));
    // start new conversation set true
    this.commonService.setRegenerateId(true);
    this.navigateToHome();
  }, err => {
    this.spinner.hide();
    this.toastService.show({ message: 'Error fetching data', classname: 'bg-danger text-light', delay: 1800 });
  })
  }
  
  ngOnDestroy(): void {
    this.sub.forEach(s => s.unsubscribe());
  }
}
