// @flow
import {
  interruptKernelEpic,
  fetchKernelspecsEpic,
  fetchContentEpic,
  setNotebookEpic,
  executeCellEpic,
  updateDisplayEpic,
  commListenEpic,
  launchWebSocketKernelEpic,
  acquireKernelInfoEpic,
  watchExecutionStateEpic,
  launchKernelWhenNotebookSetEpic,
  saveContentEpic
} from "@nteract/core/epics";

// TODO: Bring desktop's wrapEpic over to @nteract/core so we can use it here
const epics = [
  interruptKernelEpic,
  fetchKernelspecsEpic,
  executeCellEpic,
  updateDisplayEpic,
  commListenEpic,
  launchWebSocketKernelEpic,
  fetchContentEpic,
  setNotebookEpic,
  acquireKernelInfoEpic,
  watchExecutionStateEpic,
  launchKernelWhenNotebookSetEpic,
  saveContentEpic
];

export default epics;
