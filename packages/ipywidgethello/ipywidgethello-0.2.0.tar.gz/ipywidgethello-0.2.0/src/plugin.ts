// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import {
  ExampleModel, ExampleView
} from './widget';

import {
  JUPYTER_EXTENSION_VERSION
} from './version';


const EXTENSION_ID = 'jupyter.extensions.hello';


/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: 'jupyter-widget-hello',
    version: JUPYTER_EXTENSION_VERSION,
    exports: {
      ExampleModel: ExampleModel,
      ExampleView: ExampleView
    }
  });
}
