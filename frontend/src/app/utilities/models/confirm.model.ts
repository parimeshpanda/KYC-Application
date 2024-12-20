export interface ConfirmModal {
   title: string,
   subtitle?: string,
   footer? : string,
   confirmButton : {
      'text' : string,
      'class' : string
   },
   cancelButton : {
      'text' : string,
      'class' : string
   }
}
