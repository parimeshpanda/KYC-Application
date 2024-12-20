import { CommonService } from '../../../utilities/services/common/common.service';
import { environment } from '../../../../environments/environment';
import { LocationStrategy } from '@angular/common';
import { Component, OnDestroy, OnInit, ViewChild, TemplateRef, ElementRef } from '@angular/core';
import { Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { ToastService } from '../../../shared/toasts/toasts.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit, OnDestroy {
  @ViewChild('modalTemplate') modalTemplate!: TemplateRef<any>;
  @ViewChild('landingContainer') landingContainer!: ElementRef;
  public baseurl = environment.baseurl;
  private subscription: Subscription[] = [];
  public threadDetails: any;
  showBig: boolean = false
  showText: boolean = false;
  constructor(private modalService: NgbModal,private router: Router, private location: LocationStrategy, private commonService: CommonService, private spinner: NgxSpinnerService,
    private toastService: ToastService
  ) {

  }

  public exploreView() {
    setTimeout(() => {
      const blur = document.querySelector('.expandView');
      blur?.classList.add('animate__fadeOut', 'animate__faster');

    }, 650);
      this.showBig = true;
      this.scrollToTop();
     setTimeout(() => {
      this.openModal();
    }, 80);
  }

  ngOnInit(): void {
    window.scrollTo(0, 0);
    localStorage.removeItem('threadData');
  }

  public redirectToHome() {
    this.router.navigate(['home']);

  }

  openModal() {
      const modalRef = this.modalService.open(this.modalTemplate, { windowClass: 'TermsPopup',size: 'xl', centered: true,   backdrop: 'static', keyboard: false, });
  }

  public agree() {
    this.getThreadDetails();
  }

  public getThreadDetails() {
      this.spinner.show();
      this.subscription[this.subscription.length] = this.commonService.startChat().subscribe((data: any) => {
      this.spinner.hide();
      if (data.status == 200)
        this.threadDetails = data;
      localStorage.removeItem('threadData');
      localStorage.setItem('threadData', JSON.stringify(data));
      this.router.navigate(['home']);
    }, err => {
      this.spinner.hide();
      this.toastService.show({ message: 'Error fetching data', classname: 'bg-danger text-light', delay: 1800 });
    })
  }
  
  public decline() {
    this.showBig = false;
  }

  scrollToTop() {
    const container = this.landingContainer.nativeElement;
    container.scrollTo({ top: 0 });
  }

  ngOnDestroy(): void {
    this.subscription.forEach((x: any) => {
      x.unsubscribe()
    })
  }

}
