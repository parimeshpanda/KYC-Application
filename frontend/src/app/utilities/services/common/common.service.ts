import { NgbAccordionModule } from '@ng-bootstrap/ng-bootstrap';
import { Inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { RestService } from "../rest.service";
import { BehaviorSubject, Observable, of, interval, Subscription } from "rxjs";
import * as _ from "lodash";

@Injectable({
  providedIn: "root",
})
export class CommonService {

  public _threadId: any;
  public isRegenerate: BehaviorSubject<any> = new BehaviorSubject(false);
  private timeLeft: number = 420; // 7 minutes in seconds
  private timerSubscription!: Subscription;
  public formattedTime$ = new BehaviorSubject<string>('07:00'); // Observable for timer display
  constructor(private restService: RestService, private http: HttpClient) { }


  startTimer(): void {
    this.resetTimer(); // Reset timer before starting
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe(); // Ensure only one timer instance
    }
    this.timerSubscription = interval(1000).subscribe(() => {
      if (this.timeLeft > 0) {
        this.timeLeft--;
        this.updateFormattedTime();
      } else {
        this.timerSubscription.unsubscribe();
      }
    });
  }

  stopTimer(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }
  }

  resetTimer(): void {
    this.timeLeft = 420; // Reset to 7 minutes
    this.updateFormattedTime();
  }

  private updateFormattedTime(): void {
    const minutes = Math.floor(this.timeLeft / 60);
    const seconds = this.timeLeft % 60;
    const formatted = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    this.formattedTime$.next(formatted);
  }

  public startConversation(params): Observable<any> {
    let url = `chat/startConversation`;
    return this.restService.postData(url,params);
  }

  public getChatHistory(id: any) {
    let url = `chat/getChatHistory/` + id;
    return this.restService.getData(url);
  }
  
  public getSteps() {
    let url = `user/steps/`;
    return this.restService.getData(url);
  }

  public startChat() {
    let url = `chat/startChat`;
    return this.restService.postData(url);
  }
  
  public uploadFile(file: any, id:any) {
    let url = `user/upload/`+ id;
    return this.restService.postData(url, file);
  }

  public uploadDocument(file: any, id:any) {
    let url = `user/upload/`+ id;
    return this.restService.postData(url, file);
  }

public pastRecords(id:any) {
  let url = `records/pastRecordById/`+ id;
  return this.restService.getData(url);
}

public pastRecordList() {
  let url = `records/pastRecordList`;
  return this.restService.getData(url);
}

public pastRecordsInsert(params): Observable<any> {
  let url = `records/pastRecordsInsert`;
  return this.restService.postData(url,params);
}

  // getter and setter
public setRegenerateId(val:any) {
  this.isRegenerate.next(val);
}

public getRegenerateId() {
  return this.isRegenerate.asObservable();
}

public getExplanationData(thread_id:any, kyc_type:string){
    let url = `explain/explaination-data/` + thread_id + `?type=` + kyc_type;
    return this.restService.getData(url);
  }

}


