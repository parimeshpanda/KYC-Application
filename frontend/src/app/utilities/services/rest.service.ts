import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError, map, } from "rxjs/operators";
import { prod } from "src/app/shared/config/app-config";
import { environment } from "src/environments/environment";
@Injectable({
  providedIn: "root",
})
export class RestService {
  public prod = prod;
  public baseUrl: string = this.prod ? "http://localhost:8000/LLM-IT/" : "http://localhost:8000/LLM-IT/";
  
  constructor(
    private http: HttpClient
  ) { }
  /**
   * Retrieves data from the specified URL.
   * 
   * @param {string} url - The URL to retrieve data from.
   * @param {Object} params - Optional parameters for the request.
   * @returns {Observable<any>} - An observable that emits the response data.
   */

  public getData(url: string, params?: any):Observable<any>{   
    return this.http.get(url, { params: params }).pipe(map(res => {
      return res;
    }),
    catchError(err => {
      console.error(err); // handle the error here
      return throwError(Error); // throw a new error
    })
    )   
}

//post method
public postData(url: string, data?: any):Observable<any> {
  return this.http.post(url, data).pipe(map(res => {
    return res;
  }),
  catchError(err => {
    console.error(err); // handle the error here
    return throwError(Error); // throw a new error
  })
  )
}

}
