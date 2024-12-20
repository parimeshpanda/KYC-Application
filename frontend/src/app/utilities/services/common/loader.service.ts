import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  private loaderSubject = new BehaviorSubject<boolean>(false);

  constructor() { }

  /**
   * @description set loader state
   * @param state 
   */
  public  setLoader(state:any) {
      this.loaderSubject.next(state);
  }
  
  /**
   *
   * @description get loader state
   * @returns
   * @memberof LoaderService
   */
  public getLoader() {
    return this.loaderSubject.asObservable();
  }
}
