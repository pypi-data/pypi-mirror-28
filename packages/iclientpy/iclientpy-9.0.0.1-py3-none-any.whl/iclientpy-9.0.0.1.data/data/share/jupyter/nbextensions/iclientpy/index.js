define(["lib"], function(__WEBPACK_EXTERNAL_MODULE_0__) { return /******/ (function(modules) { // webpackBootstrap
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
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports) {

module.exports = lib;

/***/ }),
/* 1 */
/***/ (function(module, exports) {

module.exports = {"name":"iclientpy","version":"0.1.0","description":"iclient for jupyter","author":"supermap","main":"src/index.js","repository":{"type":"git","url":"https://gitee.com/isupermap/iClientPython.git"},"keywords":["jupyter","widgets","ipython","ipywidgets"],"files":["src/**/*.js","dist/*.js"],"scripts":{"clean":"rimraf dist/","package":"webpack","ddl":"webpack --config ./ddl.config.js","test":"echo \"Error: no test specified\" && exit 1"},"devDependencies":{"babel-core":"^6.26.0","babel-loader":"^7.0.0","babel-plugin-transform-class-properties":"^6.24.1","babel-preset-es2015":"^6.24.1","copy-webpack-plugin":"^4.2.3","css-loader":"^0.28.7","file-loader":"^1.1.5","rimraf":"^2.6.2","style-loader":"^0.19.0","url-loader":"^0.6.2","webpack":"^3.5.5"},"dependencies":{"@jupyter-widgets/base":"^1.0.0","@supermap/iclient-leaflet":"^9.0.0","jupyter-leaflet":"^0.5.0","leaflet.heat":"^0.2.0","lodash":"^4.17.4","underscore":"^1.8.3","vector-tile":"^1.3.0"}}

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(3);


/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
__webpack_require__.p = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/iclientpy/';

// Load css
__webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet/dist/leaflet.css\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
__webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet-draw/dist/leaflet.draw.css\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

// Forcibly load the marker icon images to be in the bundle.
__webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet/dist/images/marker-shadow.png\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
__webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet/dist/images/marker-icon.png\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));
__webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet/dist/images/marker-icon-2x.png\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

// Export widget models and views, and the npm package version number.
module.exports = __webpack_require__(4);
module.exports['version'] = __webpack_require__(1).version;

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _leaflet = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"leaflet\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

var _leaflet2 = _interopRequireDefault(_leaflet);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var leaflet = __webpack_require__(5);
var _ = __webpack_require__(6);
var version = __webpack_require__(1).version;

__webpack_require__(7);
__webpack_require__(8);
var mapv = __webpack_require__(!(function webpackMissingModule() { var e = new Error("Cannot find module \"mapv\""); e.code = 'MODULE_NOT_FOUND'; throw e; }()));

var SuperMapCloudTileLayerView = leaflet.LeafletTileLayerView.extend({

    create_obj: function create_obj() {
        var url = this.model.get('url');
        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }
        this.obj = _leaflet2.default.supermap.cloudTileLayer(url, options);
    }

});

var SuperMapTileMapLayerView = leaflet.LeafletTileLayerView.extend({
    create_obj: function create_obj() {
        var url = this.model.get('url');
        this.obj = _leaflet2.default.supermap.tiledMapLayer(url);
    }
});

var SuperMapRankSymbolThemeLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function create_obj() {
        var name = this.model.get('name');
        var symbolType = this.model.get('symbol_type');

        var options = this.get_options();
        if (!options.attribution) {
            delete options.attribution;
        }
        this.obj = _leaflet2.default.supermap.rankSymbolThemeLayer(name, SuperMap.ChartType[symbolType], options);
        this.obj.addTo(this.map_view.obj);
        this.add_fetures();
    },

    add_fetures: function add_fetures() {
        var symbolSetting = this.model.get('symbol_setting');
        var themeField = this.model.get('theme_field');
        this.obj.themeField = themeField;
        this.obj.symbolSetting = symbolSetting;
        this.obj.symbolSetting.codomain = this.model.get('codomain');
        var rrange = this.model.get('rrange');
        this.obj.symbolSetting.minR = rrange[0];
        this.obj.symbolSetting.maxR = rrange[1];
        this.obj.symbolSetting.fillColor = this.model.get('color');
        this.obj.clear();
        var data = this.model.get('data');
        var address_key = 0;
        var value_key = 1;
        var lng_key = 2;
        var lat_key = 3;
        var features = [];
        for (var i = 0, len = data.length; i < len; i++) {
            var geo = this.map_view.obj.options.crs.project(_leaflet2.default.latLng(data[i][lat_key], data[i][lng_key]));
            var attrs = { NAME: data[i][address_key] };
            attrs[themeField] = data[i][value_key];
            var feature = _leaflet2.default.supermap.themeFeature(geo, attrs);
            features.push(feature);
        }
        this.obj.addFeatures(features);
    },

    model_events: function model_events() {
        this.listenTo(this.model, 'change:codomain', function () {
            this.add_fetures();
        }, this);
        this.listenTo(this.model, 'change:rrange', function () {
            this.add_fetures();
        }, this);
        this.listenTo(this.model, 'change:color', function () {
            this.add_fetures();
        }, this);
    }
});

var SuperMapHeatLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function create_obj() {
        var heatPoints = this.model.get('heat_points');
        var options = this.get_options();
        if (!options.gradient || this.isNull(options.gradient)) {
            delete options.gradient;
        }
        this.obj = _leaflet2.default.heatLayer(heatPoints, options);
    },

    isNull: function isNull(obj) {
        for (var name in obj) {
            return false;
        }
        return true;
    },

    refresh: function refresh() {
        var options = this.get_options();
        if (!options.gradient || this.isNull(options.gradient)) {
            delete options.gradient;
        }
        this.obj.setOptions(options);
        this.obj.redraw();
    },

    model_events: function model_events() {
        this.listenTo(this.model, 'change:radius', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:min_opacity', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:blur', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:max', function () {
            this.refresh();
        }, this);
    }
});

var SuperMapMapVLayerView = leaflet.LeafletLayerView.extend({
    create_obj: function create_obj() {
        var dataSet = this.model.get('data_set');
        var options = this.get_options();
        var mapvOptions = this.model.get('map_v_options');
        var mapvOptions = this.model.get('map_v_options');
        var mapvDataSet = new mapv.DataSet(dataSet);
        this.obj = _leaflet2.default.supermap.mapVLayer(mapvDataSet, mapvOptions, options);
    },

    refresh: function refresh() {
        var mapvOptions = this.model.get('map_v_options');
        mapvOptions.size = this.model.get('size');
        mapvOptions.globalAlpha = this.model.get('global_alpha');
        mapvOptions.fillStyle = this.model.get('fill_style');
        mapvOptions.shadowColor = this.model.get('shadow_color');
        mapvOptions.shadowBlur = this.model.get('shadow_blur');
        // mapvOptions.lineWidth = this.model.get('line_width');
        var dataSet = this.model.get('data_set');
        var mapvDataSet = new mapv.DataSet(dataSet);
        this.obj.update({ data: mapvDataSet, options: mapvOptions });
    },

    model_events: function model_events() {
        this.listenTo(this.model, 'change:size', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:global_alpha', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:fill_style', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:shadow_color', function () {
            this.refresh();
        }, this);
        this.listenTo(this.model, 'change:shadow_blur', function () {
            this.refresh();
        }, this);
        // this.listenTo(this.model, 'change:line_width', function () {
        //     this.refresh();
        // }, this);
    }

});

var SuperMapMapView = leaflet.LeafletMapView.extend({
    create_obj: function create_obj() {
        var that = this;
        var options = this.get_options();
        options.crs = _leaflet2.default.CRS[options.crs];
        that.obj = _leaflet2.default.map(this.el, options);
    }
});

var SuperMapCloudTileLayerModel = leaflet.LeafletTileLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletTileLayerModel.prototype.defaults, {
        _view_name: 'SuperMapCloudTileLayerView',
        _model_name: 'SuperMapCloudTileLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        map_name: '',
        type: ''
    })
});

var SuperMapTileMapLayerModel = leaflet.LeafletTileLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletTileLayerModel.defaults, {
        _view_name: 'SuperMapTileMapLayerView',
        _model_name: 'SuperMapTileMapLayerModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy'
    })
});

var SuperMapRankSymbolThemeLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapRankSymbolThemeLayerView",
        _model_name: "SuperMapRankSymbolThemeLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,

        name: '',
        data: [],
        theme_field: '',
        symbol_type: '',
        symbol_setting: {}
    })
});

var SuperMapMapVLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapMapVLayerView",
        _model_name: "SuperMapMapVLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,

        data_set: [],
        size: 1,
        global_alpha: 0.0,
        fill_style: '',
        shadow_color: '',
        shadow_blur: 0
    })
});

var SuperMapHeatLayerModel = leaflet.LeafletLayerModel.extend({
    defaults: _.extend({}, leaflet.LeafletLayerModel.defaults, {
        _view_name: "SuperMapHeatLayerView",
        _model_name: "SuperMapHeatLayerModel",
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,

        radius: 0,
        min_opacity: 0.5,
        heat_points: []
    })
});

var SuperMapMapModel = leaflet.LeafletMapModel.extend({
    defaults: _.extend({}, leaflet.LeafletMapModel.prototype.defaults, {
        _view_name: 'SuperMapMapView',
        _model_name: 'SuperMapMapModel',
        _view_module: 'iclientpy',
        _model_module: 'iclientpy',
        _view_module_version: version,
        _model_module_version: version,
        crs: ''
    })
});

module.exports = _.extend({}, leaflet, {
    SuperMapRankSymbolThemeLayerView: SuperMapRankSymbolThemeLayerView,
    SuperMapCloudTileLayerView: SuperMapCloudTileLayerView,
    SuperMapTileMapLayerView: SuperMapTileMapLayerView,
    SuperMapHeatLayerView: SuperMapHeatLayerView,
    SuperMapMapVLayerView: SuperMapMapVLayerView,
    SuperMapMapView: SuperMapMapView,

    SuperMapRankSymbolThemeLayerModel: SuperMapRankSymbolThemeLayerModel,
    SuperMapCloudTileLayerModel: SuperMapCloudTileLayerModel,
    SuperMapTileMapLayerModel: SuperMapTileMapLayerModel,
    SuperMapHeatLayerModel: SuperMapHeatLayerModel,
    SuperMapMapVLayerModel: SuperMapMapVLayerModel,
    SuperMapMapModel: SuperMapMapModel
});

/***/ }),
/* 5 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = (__webpack_require__(0))(797);

/***/ }),
/* 6 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = (__webpack_require__(0))(292);

/***/ }),
/* 7 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = (__webpack_require__(0))(1128);

/***/ }),
/* 8 */
/***/ (function(module, exports, __webpack_require__) {

module.exports = (__webpack_require__(0))(1133);

/***/ })
/******/ ])});;
//# sourceMappingURL=index.js.map