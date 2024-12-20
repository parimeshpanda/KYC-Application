import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subscription } from 'rxjs';
import { ToastService } from 'src/app/shared/toasts/toasts.service';
import { CommonService } from 'src/app/utilities/services/common/common.service';
import { environment } from 'src/environments/environment';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
@Component({
  selector: 'app-explanation',
  templateUrl: './explanation.component.html',
  styleUrls: ['./explanation.component.scss']
})
export class ExplanationComponent {
  public baseurl = environment.baseurl;
  private subscription: Subscription[] = [];
  public isNextVal: any = 0;
  public isClickedNext: boolean = false;
  public isKYCSuccess:boolean = true;
  public guidelineDetails : any;
  public explaination:any;
  public docCollDetails: Record<string, any> = {};
  public agentDetails: any;
  public comparatorAgentDetails: any;
  timer: NodeJS.Timeout;
  threadId!: string;
  kyc_type: string;
  Object = Object;
  constructor(private modalService: NgbModal, public route: ActivatedRoute, public router: Router, private commonService: CommonService,
    private spinner: NgxSpinnerService, private toastService: ToastService
  ) {

  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.threadId = params['id'];
      this.kyc_type = params['type']
      if (this.threadId) {
        this.getKycDisplayData(this.threadId, this.kyc_type);
      }
    });
  }

  /* get kyc data */
  public getKycDisplayData(threadId: any,kyc_type:string){
    this.subscription[this.subscription.length] = this.commonService.getExplanationData(threadId,kyc_type).subscribe((data: any) => {
      this.spinner.hide();
      if (data.status == 200){
        this.agentDetails = data.data.agentDetails;
        this.docCollDetails = data.data.docCollDetails;
        this.comparatorAgentDetails = data.data.comparatorAgentDetails;
        this.isKYCSuccess = data.data.isKYCSuccess;
        this.guidelineDetails = data.data.guidelineDetails;
        this.explaination = data.data.explaination;
      }else{
      this.toastService.show({ message: 'Something went wrong', classname: 'bg-danger text-light', delay: 1800 });
      }
    }, err => {
      this.spinner.hide();
      this.toastService.show({ message: 'Something went wrong', classname: 'bg-danger text-light', delay: 1800 });
    })
  }

  private setLavel1Animation(): void {
    document.querySelectorAll(".ciclegraph").forEach((ciclegraph) => {
      let infoBoxs = ciclegraph.querySelectorAll<HTMLElement>(".level1");
      let angle = 30 - 30,
        dangle = 4 / infoBoxs.length;
      for (let i = 0; i < infoBoxs.length; ++i) {
        let infoBox = infoBoxs[i];
        angle += dangle;
        infoBox.style.transition = "transform 1s ease";
        infoBox.style.transform = `0px, 0px)`;
        infoBox.style.transition = " ";
        infoBox.style.transform = `translate(-120px, -25px)`;
      }
    });

  }

  reset() {
    this.isNextVal = 0;
    this.isClickedNext = false;
  }

  public next(val) {
    if (val == 0) {
      this.setLavel1Animation();
    }
    setTimeout(() => {
      this.isNextVal = 1 + val;
      this.isClickedNext = true;
    }, 500);
  }

/* kyc validation more info btn */
  public kycValidationInfo(kycValidation) {
    const modalRef = this.modalService.open(kycValidation, {
      windowClass: 'kycValidationClass',
      size: 'lg', centered: true, backdrop: 'static', keyboard: false, scrollable: true
    });
  }
  /* kyc validation more info btn */
  public guidelinesAgentInfo(guidelinesAgent) {
    const modalRef = this.modalService.open(guidelinesAgent, {
      windowClass: 'kycValidationClass',
      size: 'lg', centered: true, backdrop: 'static', keyboard: false, scrollable: true
    });
  }
  /* kyc validation more info btn */
  public comparatorAgentInfo(comparatorAgent) {
    const modalRef = this.modalService.open(comparatorAgent, {
      windowClass: 'kycValidationClass, comparatorAgentClass',
      size: 'lg', centered: true, backdrop: 'static', keyboard: false, scrollable: true
    });
  }

  /* back to past record */
  public backToPastRecord(){
    this.router.navigate(['past-records'])
  }

}
