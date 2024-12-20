import { ChangeDetectorRef, Component, ElementRef, OnDestroy, OnInit, SimpleChanges, ViewChild, ViewChildren } from '@angular/core';
import { CommonService } from '../../../utilities/services/common/common.service';
import { Subscription } from 'rxjs';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { NgxSpinnerService } from 'ngx-spinner';
import * as _ from 'lodash';
import { LocationStrategy } from '@angular/common';
import { environment } from '../../../../environments/environment';
import { ToastService } from 'src/app/shared/toasts/toasts.service';
import { DomSanitizer } from '@angular/platform-browser';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
 
  public animationClass: string = '';
  public stepName:string = '';
  @ViewChild('answerInput', { static: false }) answerInput!: ElementRef<HTMLTextAreaElement>
  public file: any = [];
  public showError: boolean = false;
  public subscription: Subscription[] = [];
  public stepsData:any;
  threadId:any;
  receivedData:any;
  constructor(private commonService: CommonService, public route: ActivatedRoute, private spinner: NgxSpinnerService, public router: Router, private toastService: ToastService, private location: LocationStrategy, private sanitizer: DomSanitizer, private cdr: ChangeDetectorRef) {

  }
  
  ngOnInit(): void {
    setTimeout(() => {
      this.commonService.startTimer(); // Start the timer when Home Component is loaded
    }, 1000);
    this.subscription[this.subscription.length] = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd && event.url === '/') {
        setTimeout(() => {
          this.commonService.startTimer(); // Reset and start the timer
        }, 1000);
      }
    });
    this.newChat();
    this.subscription[this.subscription.length] = this.commonService.getRegenerateId().subscribe((data: any) => {
      if(data){
        this.newChat();
      }
    })
   
  }

  public newChat(){
    const threadId = localStorage.getItem('threadData');
    this.threadId = JSON.parse(threadId);
    this.APICallForSteps();
    setTimeout(() => {
      this.loadThreadQuestions();
    }, 100); 
    setTimeout(() => {
      this.commonService.startTimer();
    }, 1000);
  }

 
  public baseurl = environment.baseurl;

  activeThreadId:any;
  activeStep:any;
  currentQuestions: any;
  currentConversationIndex = 0;
  currentAnswer = '';
  typingText = ''; // This will hold the text being typed
  typingIndex = 0; // Index for typing effect
  typingInterval: any; // To store the interval reference
  threadData:any;
  showFileUpload: boolean = false;
  reviewData:any;
  reviewDetails:any;
  showConfirmLoader :boolean = false;
  showResult:boolean = false;
  animateBackground() {
    this.animationClass = 'animate__animated animate__fadeOut'; // Start fade-out
    setTimeout(() => {
      this.animationClass = 'animate__animated animate__fadeIn'; // Trigger fade-in
    }, 500); // Delay for fade-in
  }

  resetAnimation() {
    this.animationClass = ''; // Reset animation class after animation ends
  }
  public APICallForSteps() {
    this.subscription[this.subscription.length] = this.commonService.getSteps().subscribe((data: any) => {
      this.spinner.show();
      if (data.status == 200) {
       this.stepsData = data['data'];
      this.activeThreadId = this.stepsData[0].id;
      this.activeStep = this.stepsData.find((t) => t.id == this.activeThreadId);
      this.stepName = this.activeStep?.name || '';
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

  loadThreadQuestions(kycStatus?:boolean) {
    if(kycStatus) {
      this.showConfirmLoader = true;
    }
    else {
      this.spinner.show();
      this.showConfirmLoader = false;
    }
    let params = 
      {
       "thread_id":  this.threadId.thread_id,
        "result": {
          "id": this.currentQuestions?.result.id || '',
          "ai_question": this.currentQuestions?.result.ai_question || '',
          "human_answer": this.currentAnswer || '',
          "stepper": this.currentQuestions?.result.stepper  || '',
          "timestamp": this.currentQuestions?.result.timestamp  || '',
          "conversation_type": this.currentQuestions?.result.conversation_type || ''
        }
      
    }
    
    this.subscription[this.subscription.length] = this.commonService.startConversation(params).subscribe((data: any) => {
     
      if (data.status == 200){
      
        this.threadData = data['data'];
        this.showConfirmLoader = false;
        this.spinner.hide();
        if (this.threadData?.result) {
          this.currentQuestions = this.threadData;
          
          this.currentConversationIndex = 0;
          if(this.threadData.result){
           setTimeout(() => {
             this.startTyping();
           }, 500); 
          }
          // Mark step as completed if stepCompleted is true
          if (this.threadData.result.stepper == 0) {
            this.stepsData[0].completed = false;
            this.stepName = this.stepsData[0].name;
            this.activeThreadId = this.stepsData[0].id;
          }
         if (this.threadData.result.stepper == 1) {
           this.stepsData[0].completed = true;
           this.stepName = this.stepsData[1].name;
           this.activeThreadId = this.stepsData[1].id;
         }
         else if(this.threadData.result.stepper == 2) {
          this.stepsData[0].completed = true;
          this.stepsData[1].completed = true;
          this.stepName = this.stepsData[2].name;
          this.activeThreadId = this.stepsData[2].id;
        }
        else if(this.threadData.result.stepper == 3) {
          this.stepsData[0].completed = true;
          this.stepsData[1].completed = true;
          this.stepsData[2].completed = true;
          this.stepName = this.stepsData[3].name;
          this.activeThreadId = this.stepsData[3].id;
        }
        else if((this.threadData.result.stepper == 4) && (this.threadData.result.conversation_type == 'Fail') || (this.threadData.result.conversation_type == 'Pass')) {
          this.stepsData[0].completed = true;
          this.stepsData[1].completed = true;
          this.stepsData[2].completed = true;
          this.stepsData[3].completed = true;
          this.stepName = this.stepsData[4].name;
          this.activeThreadId = this.stepsData[4].id;
          setTimeout(() => {
            this.showConfirmLoader = false;
            this.showResult = true;
            this.pastRecordsInsert();
          }, 1000)
        }
        if(this.threadData.result.conversation_type == 'upload') {
          setTimeout(() => {
            this.showFileUpload = true;
          }, 1000);
        }
        else {
          this.showFileUpload = false;
        }
        if(this.threadData.result.conversation_type == 'review') {
          this.getHistory();
        }
      
      }
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

 public getHistory() {
  this.spinner.show();
  this.subscription[this.subscription.length] = this.commonService.getChatHistory(this.threadId.thread_id).subscribe((data: any) => {
    if (data) {
    this.reviewDetails = data;
    this.reviewData = this.reviewDetails?.result?.filter(item => item.id !== '');
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

     private pastRecordsInsert() {
      let params = 
      {
          "name": this.currentQuestions?.result.comparator_state.kyc_for || '',
          "thread_id": this.threadId.thread_id || '',
          "type": this.currentQuestions?.result.comparator_state.kyc_type || '',
          "kycStatus": this.currentQuestions?.result.comparator_state.kyc_result  || '',
          "dateAdded": this.currentQuestions?.result.timestamp  || '',
          "explaination": this.currentQuestions?.result.comparator_state.result_explanation
      }
      this.spinner.show();
      this.subscription[this.subscription.length] = this.commonService.pastRecordsInsert(params).subscribe((data: any) => {
     
        if (data.status == 200) {
        
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

  startTyping() {
    this.typingText = ''; // Reset the typing text
    const question = this.currentQuestions?.result?.ai_question || '';
    this.typingIndex = 0;
     // Ensure no overlapping intervals
     if (this.typingInterval) {
      clearInterval(this.typingInterval);
  }

      this.typingInterval = setInterval(() => {
      if (this.typingIndex < question.length) {
        this.typingText += question[this.typingIndex];
        this.typingIndex++;
        this.cdr.detectChanges(); // Explicitly trigger change detection
      } else {
        clearInterval(this.typingInterval); // Stop typing when complete
      }
    }, 10); // Adjust typing speed by changing the interval
  }

  submitAnswer(event?: Event) {
    const keyboardEvent = event as KeyboardEvent;
    keyboardEvent.preventDefault();
    const currentQuestion = this.currentQuestions.result;
    if (!currentQuestion) return;

    currentQuestion.human_answer = this.currentAnswer;
    this.loadThreadQuestions();
    this.currentAnswer = '';
    // Remove focus from the textarea to show the placeholder
    if (this.answerInput) {
      const textarea = this.answerInput.nativeElement;
      textarea.value = ''; // Clear the textarea value
      textarea.focus(); // Set focus back to the textarea
    }

      const currentThread = this.stepsData.find((t) => t.id == this.threadData.stepper + 1);
      if (currentThread) currentThread.completed = true;

      // Move to the next thread
      if(this.currentQuestions.stepCompleted){
       
      const nextThread = this.stepsData.find((t) => t.id === this.activeThreadId + 1);
      
      if (nextThread) {
        this.activeThreadId = nextThread.id;
        this.loadThreadQuestions();
        this.animateBackground();
      }
    }
  }

  

  /**
   * @description function to drag file
   */
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.showError = false;
  }

  /**
   * @description function to drop file
   */
  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.showError = false;
    this.file = [];
    let file: any = event.dataTransfer?.files || [];
    if (file[0].type == 'application/pdf'||file[0].type == 'image/gif'||file[0].type == 'image/tiff'
    ||file[0].type == 'image/tif'||file[0].type == 'image/jpg'||file[0].type == 'image/jpeg'||file[0].type == 'image/png'
    ||file[0].type == 'image/bmp'||file[0].type == 'image/webp') {
      this.file = file;
    }
  }

  onFileChange(event: any) {
    this.showError = false;
    this.file = [];
    let file: any = event.target?.files || [];
    if (file[0].type == 'application/pdf'||file[0].type == 'image/gif'||file[0].type == 'image/tiff'
    ||file[0].type == 'image/tif'||file[0].type == 'image/jpg'||file[0].type == 'image/jpeg'||file[0].type == 'image/png'
    ||file[0].type == 'image/bmp'||file[0].type == 'image/webp') {
      this.file = file;
    }
  }
  
    
     /**
   * @description navigate to explaination
   */
     public navgateToExplanation(thread_id:any, kyc_type: string) {

      this.router.navigate(['explanation'], {
        queryParams: { id: thread_id, type: kyc_type}
      });
    }

    /**
   * @description function to remove selected file
   */
  public removeFile() {
    this.file = [];
    this.showError = false;
  }

  /**
   * @description function to upload selected file to backend
   */
  public uploadFile() {
    if(this.file.length == 0) {
      this.showError = true;
      return;
    }
    else {
      this.showError = false;
    }
  
    const formData = new FormData();
    formData.append('file', this.file[0]);
    this.spinner.show();
    this.subscription[this.subscription.length] = this.commonService
      .uploadFile(formData,this.threadId.thread_id)
      .subscribe(
        (res: any) => {
         
          if (res.status == 200) {
            var that = this;
            if (res.data) {
              let fileData = res.data;
              this.spinner.hide();
              const currentQuestion = this.currentQuestions.result;
              if (!currentQuestion) return;
              this.currentAnswer = fileData.file_name;
              currentQuestion.human_answer = this.currentAnswer;
              this.loadThreadQuestions();
              this.file = [];
              this.currentAnswer = '';
              // Remove focus from the textarea to show the placeholder
              if (this.answerInput) {
                const textarea = this.answerInput.nativeElement;
                textarea.value = ''; // Clear the textarea value
                textarea.blur(); // Remove focus to display placeholder
              }
            }
          } 
          else {
            this.spinner.hide();
            this.toastService.show({ message: 'Something went wrong. Please try again.', classname: 'bg-danger text-light toastClass', delay: 1800 });
          }
        },
        (error) => {
          this.spinner.hide();
        }
      );
  }
  

  ngOnDestroy(): void {
    this.subscription.forEach((x: any) => {
      x.unsubscribe()
    })
  }

}
