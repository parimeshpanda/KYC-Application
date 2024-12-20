import { Component, OnInit } from '@angular/core';

import { ToastService } from './toasts.service';

@Component({
	selector: 'app-toasts', 
     templateUrl: './toasts.component.html',

})


export class ToastsComponent implements OnInit {
    toasts: any[]=[]
	constructor(public toastService:ToastService){

    }
    ngOnInit(): void {
        this.toasts = this.toastService.toasts;;
        
    }
}