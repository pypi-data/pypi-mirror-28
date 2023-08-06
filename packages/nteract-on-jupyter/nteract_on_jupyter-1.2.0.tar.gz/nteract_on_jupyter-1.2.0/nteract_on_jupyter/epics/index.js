// @flow
import { loadEpic } from "./contents";
import { listKernelSpecsEpic } from "./kernelspecs";
import { setNotebookEpic } from "./notebook";

import {
  executeCellEpic,
  updateDisplayEpic,
  commListenEpic,
  launchWebSocketKernelEpic,
  acquireKernelInfoEpic,
  watchExecutionStateEpic
} from "@nteract/core/epics";

// TODO: Bring desktop's wrapEpic over to @nteract/core so we can use it here
const epics = [
  executeCellEpic,
  updateDisplayEpic,
  commListenEpic,
  launchWebSocketKernelEpic,
  loadEpic,
  listKernelSpecsEpic,
  setNotebookEpic,
  acquireKernelInfoEpic,
  watchExecutionStateEpic
];

export default epics;
