import { Directive, ElementRef, HostListener, Renderer2 } from '@angular/core';

@Directive({
  selector: '[appNowhitespace]'
})
export class AppNowhitespaceDirective {

  constructor(private el: ElementRef, private renderer: Renderer2) { }

  @HostListener('keydown') onMouseEnter(event: KeyboardEvent) {
    let value = this.el.nativeElement.value;
    let removespace = value.trim();
    this.el.nativeElement.value = removespace;
    return this.el.nativeElement.value;
  }

}
