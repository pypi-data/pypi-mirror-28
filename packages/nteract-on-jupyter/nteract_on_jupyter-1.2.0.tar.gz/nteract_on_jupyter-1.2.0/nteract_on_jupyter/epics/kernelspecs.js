/* @flow */

import { kernelspecs } from "rx-jupyter";

import { of } from "rxjs/add/observable/of";
import { merge } from "rxjs/add/observable/merge";

import {
  tap,
  map,
  switchMap,
  mapTo,
  mergeMap,
  catchError
} from "rxjs/operators";
import { ofType } from "redux-observable";

import type { ActionsObservable } from "redux-observable";

import type { ALL_ACTIONS } from "../actions/";

import type {
  LIST_KERNELSPECS,
  GENERIC_AJAX_FAIL
} from "../actions/kernelspecs";

function listKernelSpecs(): LIST_KERNELSPECS {
  return { type: "LIST_KERNELSPECS" };
}

function genericAjaxFail(ajaxError: any): GENERIC_AJAX_FAIL {
  return {
    type: "GENERIC_AJAX_FAIL",
    payload: ajaxError.response,
    status: ajaxError.status
  };
}

type ServerConfig = {
  endpoint: string,
  crossDomain?: boolean
};

export function listKernelSpecsEpic(
  action$: ActionsObservable<ALL_ACTIONS>,
  store: Store<*, *>
) {
  return action$.pipe(
    ofType("LIST_KERNELSPECS"),
    switchMap((action: LIST_KERNELSPECS) => {
      const host = store.getState().app.host;
      // Normalizing to match rx-jupyter vs. host record
      const serverConfig = {
        endpoint: host.serverUrl,
        token: host.token,
        crossDomain: false
      };

      // $FlowFixMe: WTF
      return kernelspecs.list(serverConfig).pipe(
        tap(xhr => {
          if (xhr.status !== 200) {
            throw new Error(xhr.response);
          }
        }),
        map(xhr => {
          return {
            type: "KERNELSPECS_LISTED",
            payload: xhr.response
          };
        }),
        catchError((xhrError: any) => of(genericAjaxFail(xhrError)))
      );
    })
  );
}
