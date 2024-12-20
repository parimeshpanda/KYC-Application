// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  baseurl: '',
  issuer: 'https://dev-95943079.okta.com/oauth2/default',
  clientId: '0oaka7vsxtLbMxs5I5d7',
  redirectUri: window.location.origin + '/login/callback',
  postLogoutRedirectUri: window.location.origin
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
