import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss']
})
export class FooterComponent implements OnInit {
  public startYear: string = '2022'
  public currentYear: string = '';
  @Input() public isLanding: boolean = false;
  public userDetails: any = null;
  
  constructor() { }

  ngOnInit(): void {
    this.currentYear = new Date().getFullYear().toString();
  }

}
