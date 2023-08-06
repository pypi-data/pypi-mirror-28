/* @flow */
import { combineReducers, createStore, applyMiddleware, compose } from "redux";
import { createEpicMiddleware, combineEpics } from "redux-observable";

import { List as ImmutableList, Map as ImmutableMap } from "immutable";

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

import {
  document,
  comms,
  config,
  app,
  entitiesKernelspecsByRef,
  modals
} from "@nteract/core/reducers";

import {
  makeAppRecord,
  AppRecord,
  makeDocumentRecord,
  DocumentRecord,
  CommsRecord,
  makeJupyterHostRecord
} from "@nteract/types/core/records";

import epics from "./epics";

export type JupyterConfigData = {
  token: string,
  page: "tree" | "view" | "edit",
  contentsPath: string,
  baseUrl: string,
  appVersion: string
};

export type AppState = {
  app: AppRecord,
  document: DocumentRecord,
  comms: CommsRecord,
  config: ImmutableMap<string, any>,
  contents: any,
  modals: any
};

const rootReducer = combineReducers({
  app,
  document,
  comms,
  config,
  modals,
  entities: combineReducers({
    kernelspecsByRef: entitiesKernelspecsByRef
  })
});

export default function configureStore({
  config
}: {
  config: JupyterConfigData
}) {
  const initialState = {
    app: makeAppRecord({
      host: makeJupyterHostRecord({
        token: config.token,
        // TODO: Use URL join, even though we know these are right
        serverUrl: location.origin + config.baseUrl
      }),
      version: `nteract-on-jupyter@${config.appVersion}`
    }),
    document: makeDocumentRecord(),
    comms: CommsRecord(),
    config: ImmutableMap({
      theme: "light"
    })
  };

  const rootEpic = combineEpics(...epics);
  const middlewares = [createEpicMiddleware(rootEpic)];

  return createStore(
    rootReducer,
    initialState,
    composeEnhancers(applyMiddleware(...middlewares))
  );
}
