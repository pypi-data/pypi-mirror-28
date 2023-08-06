define(["@jupyter-widgets/base"], function(__WEBPACK_EXTERNAL_MODULE_1__) { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Vidar Tonaas Fauske.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * The version of the attribute spec that this package
 * implements. This is the value used in
 * _model_module_version/_view_module_version.
 *
 * Update this value when attributes are added/removed from
 * your models, or serialized format changes.
 */
exports.JUPYTER_EXTENSION_VERSION = '1.0.0';


/***/ }),
/* 1 */
/***/ (function(module, exports) {

module.exports = __WEBPACK_EXTERNAL_MODULE_1__;

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Vidar Tonaas Fauske.
// Distributed under the terms of the Modified BSD License.
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || Object.assign || function(t) {
    for (var s, i = 1, n = arguments.length; i < n; i++) {
        s = arguments[i];
        for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
            t[p] = s[p];
    }
    return t;
};
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(1);
var version_1 = __webpack_require__(0);
var ExampleModel = (function (_super) {
    __extends(ExampleModel, _super);
    function ExampleModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ExampleModel.prototype.defaults = function () {
        return __assign({}, _super.prototype.defaults.call(this), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'Hello World' });
    };
    ExampleModel.serializers = __assign({}, base_1.DOMWidgetModel.serializers);
    ExampleModel.model_name = 'ExampleModel';
    ExampleModel.model_module = 'jupyter-widget-hello';
    ExampleModel.model_module_version = version_1.JUPYTER_EXTENSION_VERSION;
    ExampleModel.view_name = 'ExampleView'; // Set to null if no view
    ExampleModel.view_module = 'jupyter-widget-hello'; // Set to null if no view
    ExampleModel.view_module_version = version_1.JUPYTER_EXTENSION_VERSION;
    return ExampleModel;
}(base_1.DOMWidgetModel));
exports.ExampleModel = ExampleModel;
var ExampleView = (function (_super) {
    __extends(ExampleView, _super);
    function ExampleView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ExampleView.prototype.render = function () {
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    };
    ExampleView.prototype.value_changed = function () {
        this.el.textContent = this.model.get('value');
    };
    return ExampleView;
}(base_1.DOMWidgetView));
exports.ExampleView = ExampleView;


/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
__export(__webpack_require__(4));
__export(__webpack_require__(0));
__export(__webpack_require__(2));


/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", { value: true });
var base_1 = __webpack_require__(1);
var widget_1 = __webpack_require__(2);
var version_1 = __webpack_require__(0);
var EXTENSION_ID = 'jupyter.extensions.hello';
/**
 * The example plugin.
 */
var examplePlugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true
};
exports.default = examplePlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: 'jupyter-widget-hello',
        version: version_1.JUPYTER_EXTENSION_VERSION,
        exports: {
            ExampleModel: widget_1.ExampleModel,
            ExampleView: widget_1.ExampleView
        }
    });
}


/***/ })
/******/ ])});;
//# sourceMappingURL=index.js.map