/*
 * Copyright 2015 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
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
define(["require", "exports"], function (require, exports) {
    "use strict";
    /// <reference path="../../../externs/ts/require/require.d.ts" />
    var Charting;
    (function (Charting) {
        // Wrappers for Plotly.js and Google Charts
        var ChartLibraryDriver = /** @class */ (function () {
            function ChartLibraryDriver(dom, chartStyle) {
                this.dom = dom;
                this.chartStyle = chartStyle;
            }
            ChartLibraryDriver.prototype.init = function (chartModule) {
                this.chartModule = chartModule;
            };
            ChartLibraryDriver.prototype.addPageChangedHandler = function (handler) {
            };
            ChartLibraryDriver.prototype.error = function (message) {
            };
            return ChartLibraryDriver;
        }());
        var PlotlyDriver = /** @class */ (function (_super) {
            __extends(PlotlyDriver, _super);
            function PlotlyDriver(dom, chartStyle) {
                return _super.call(this, dom, chartStyle) || this;
            }
            PlotlyDriver.prototype.requires = function (url, chartStyle) {
                return ['d3', 'plotly'];
            };
            PlotlyDriver.prototype.draw = function (data, options) {
                /*
                 * TODO(gram): if we start moving more chart types over to Plotly.js we should change the
                 * shape of the data we pass to render so we don't need to reshape it here. Also, a fair
                 * amount of the computation done here could be moved to Python code. We should just be
                 * passing in the mostly complete layout object in JSON, for example.
                 */
                var xlabels = [];
                var points = [];
                var layout = {
                    xaxis: {},
                    yaxis: {},
                    height: 300,
                    margin: {
                        b: 60,
                        t: 60,
                        l: 60,
                        r: 60
                    }
                };
                if (options.title) {
                    layout.title = options.title;
                }
                var minX = undefined;
                var maxX = undefined;
                if ('hAxis' in options) {
                    if ('minValue' in options.hAxis) {
                        minX = options.hAxis.minValue;
                    }
                    if ('maxValue' in options.hAxis) {
                        maxX = options.hAxis.maxValue;
                    }
                    if (minX != undefined || maxX != undefined) {
                        layout.xaxis.range = [minX, maxX];
                    }
                }
                var minY = undefined;
                var maxY = undefined;
                if ('vAxis' in options) {
                    if ('minValue' in options.vAxis) {
                        minY = options.vAxis.minValue;
                    }
                    else if ('minValues' in options.vAxis) {
                        minY = options.vAxis.minValues[0];
                    }
                    if ('maxValue' in options.vAxis) {
                        maxY = options.vAxis.maxValue;
                    }
                    else if ('maxValues' in options.vAxis) {
                        maxY = options.vAxis.maxValues[0];
                    }
                    if (minY != undefined || maxY != undefined) {
                        layout.yaxis.range = [minY, maxY];
                    }
                    if ('minValues' in options.vAxis) {
                        minY = options.vAxis.minValues[1]; // for second axis below
                    }
                    if ('maxValues' in options.vAxis) {
                        maxY = options.vAxis.maxValues[1]; // for second axis below
                    }
                }
                if (options.xAxisTitle) {
                    layout.xaxis.title = options.xAxisTitle;
                }
                if (options.xAxisSide) {
                    layout.xaxis.side = options.xAxisSide;
                }
                if (options.yAxisTitle) {
                    layout.yaxis.title = options.yAxisTitle;
                }
                if (options.yAxesTitles) {
                    layout.yaxis.title = options.yAxesTitles[0];
                    layout.yaxis2 = {
                        title: options.yAxesTitles[1],
                        side: 'right',
                        overlaying: 'y'
                    };
                    if (minY != undefined || maxY != undefined) {
                        layout.yaxis2.range = [minY, maxY];
                    }
                }
                if ('width' in options) {
                    layout.width = options.width;
                }
                if ('height' in options) {
                    layout.height = options.height;
                    if ('width' in options) {
                        layout.autosize = false;
                    }
                }
                var pdata = [];
                if (this.chartStyle == 'line' || this.chartStyle == 'scatter') {
                    var hoverCol = 0;
                    var x = [];
                    // First col is X, other cols are Y's and optional hover text only column
                    var y = [];
                    var hover = [];
                    for (var c = 1; c < data.cols.length; c++) {
                        x[c - 1] = [];
                        y[c - 1] = [];
                        var line = {
                            x: x[c - 1],
                            y: y[c - 1],
                            name: data.cols[c].label,
                            type: 'scatter',
                            mode: this.chartStyle == 'scatter' ? 'markers' : 'lines'
                        };
                        if (options.hoverOnly) {
                            hover[c - 1] = [];
                            line.text = hover[c - 1];
                            line.hoverinfo = 'text';
                        }
                        if (options.yAxesTitles && (c % 2) == 0) {
                            line.yaxis = 'y2';
                        }
                        pdata.push(line);
                    }
                    for (var c = 1; c < data.cols.length; c++) {
                        if (c == hoverCol) {
                            continue;
                        }
                        for (var r = 0; r < data.rows.length; r++) {
                            var entry = data.rows[r].c;
                            if ('v' in entry[c]) {
                                var xVal = entry[0].v;
                                var yVal = entry[c].v;
                                if (options.hoverOnly) {
                                    // Each column is a dict with two values, one for y and one for
                                    // hover. Extract these.
                                    var hoverVal;
                                    var yDict = yVal;
                                    for (var prop in yDict) {
                                        var val = yDict[prop];
                                        if (prop == options.hoverOnly) {
                                            hoverVal = val;
                                        }
                                        else {
                                            yVal = val;
                                        }
                                    }
                                    // TODO(gram): we may want to add explicit hover text this even without hoverOnly.
                                    var xlabel = options.xAxisTitle || data.cols[0].label;
                                    var ylabel = options.yAxisTitle || data.cols[c].label;
                                    var prefix = '';
                                    if (options.yAxisTitle) {
                                        prefix += data.cols[c].label + ': ';
                                    }
                                    hover[c - 1].push(prefix +
                                        options.hoverOnly + '=' + hoverVal + ', ' +
                                        xlabel + '=' + xVal + ', ' +
                                        ylabel + '=' + yVal);
                                }
                                x[c - 1].push(xVal);
                                y[c - 1].push(yVal);
                            }
                        }
                    }
                }
                else if (this.chartStyle == 'heatmap') {
                    var size = 200 + data.cols.length * 50;
                    if (size > 800)
                        size = 800;
                    layout.height = size;
                    layout.width = size;
                    layout.autosize = false;
                    for (var i = 0; i < data.cols.length; i++) {
                        xlabels[i] = data.cols[i].label;
                    }
                    var ylabels = [].concat(xlabels);
                    // Plotly draws the first row at the bottom, not the top, so we need
                    // to reverse the y and z array ordering.
                    // We will need to tweak this a bit if we later support non-square maps.
                    ylabels.reverse();
                    var hovertext = [];
                    var hoverx = options.xAxisTitle || 'x';
                    var hovery = options.yAxisTitle || 'y';
                    for (var i = 0; i < data.rows.length; i++) {
                        var entry = data.rows[i].c;
                        var row = [];
                        var hoverrow = [];
                        for (var j = 0; j < data.cols.length; j++) {
                            row[j] = entry[j].v;
                            hoverrow[j] = hoverx + '= ' + xlabels[j] + ', ' + hovery + '= ' +
                                ylabels[i] + ': ' + row[j];
                        }
                        points[i] = row;
                        hovertext[i] = hoverrow;
                    }
                    points.reverse();
                    layout.hovermode = 'closest';
                    pdata = [{
                            x: xlabels,
                            y: ylabels,
                            z: points,
                            type: 'heatmap',
                            text: hovertext,
                            hoverinfo: 'text'
                        }];
                    if (options.colorScale) {
                        pdata[0].colorscale = [
                            [0, options.colorScale.min],
                            [1, options.colorScale.max]
                        ];
                    }
                    else {
                        pdata[0].colorscale = [
                            [0, 'red'],
                            [0.5, 'gray'],
                            [1, 'blue']
                        ];
                    }
                    if (options.hideScale) {
                        pdata[0].showscale = false;
                    }
                    if (options.annotate) {
                        layout.annotations = [];
                        for (var i = 0; i < pdata[0].y.length; i++) {
                            for (var j = 0; j < pdata[0].x.length; j++) {
                                var currentValue = pdata[0].z[i][j];
                                var textColor = (currentValue == 0.0) ? 'black' : 'white';
                                var result = {
                                    xref: 'x1',
                                    yref: 'y1',
                                    x: pdata[0].x[j],
                                    y: pdata[0].y[i],
                                    text: pdata[0].z[i][j].toPrecision(3),
                                    showarrow: false,
                                    font: {
                                        color: textColor
                                    }
                                };
                                layout.annotations.push(result);
                            }
                        }
                    }
                }
                this.chartModule.newPlot(this.dom.id, pdata, layout, { displayModeBar: false });
                if (this.readyHandler) {
                    this.readyHandler();
                }
            };
            PlotlyDriver.prototype.getStaticImage = function (callback) {
                this.chartModule.Snapshot.toImage(document.getElementById(this.dom.id), { format: 'png' }).once('success', function (url) {
                    callback(this.model, url);
                });
            };
            PlotlyDriver.prototype.addChartReadyHandler = function (handler) {
                this.readyHandler = handler;
            };
            return PlotlyDriver;
        }(ChartLibraryDriver));
        var GChartsDriver = /** @class */ (function (_super) {
            __extends(GChartsDriver, _super);
            function GChartsDriver(dom, chartStyle) {
                var _this = _super.call(this, dom, chartStyle) || this;
                _this.nameMap = {
                    annotation: 'AnnotationChart',
                    area: 'AreaChart',
                    columns: 'ColumnChart',
                    bars: 'BarChart',
                    bubbles: 'BubbleChart',
                    calendar: 'Calendar',
                    candlestick: 'CandlestickChart',
                    combo: 'ComboChart',
                    gauge: 'Gauge',
                    geo: 'GeoChart',
                    histogram: 'Histogram',
                    line: 'LineChart',
                    map: 'Map',
                    org: 'OrgChart',
                    paged_table: 'Table',
                    pie: 'PieChart',
                    sankey: 'Sankey',
                    scatter: 'ScatterChart',
                    stepped_area: 'SteppedAreaChart',
                    table: 'Table',
                    timeline: 'Timeline',
                    treemap: 'TreeMap'
                };
                _this.scriptMap = {
                    annotation: 'annotationchart',
                    calendar: 'calendar',
                    gauge: 'gauge',
                    geo: 'geochart',
                    map: 'map',
                    org: 'orgchart',
                    paged_table: 'table',
                    sankey: 'sankey',
                    table: 'table',
                    timeline: 'timeline',
                    treemap: 'treemap'
                };
                return _this;
            }
            GChartsDriver.prototype.requires = function (url, chartStyle) {
                var chartScript = 'corechart';
                if (chartStyle in this.scriptMap) {
                    chartScript = this.scriptMap[chartStyle];
                }
                return [url + 'visualization!' + chartScript];
            };
            GChartsDriver.prototype.init = function (chartModule) {
                _super.prototype.init.call(this, chartModule);
                var constructor = this.chartModule[this.nameMap[this.chartStyle]];
                this.chart = new constructor(this.dom);
            };
            GChartsDriver.prototype.error = function (message) {
                this.chartModule.errors.addError(this.dom, 'Unable to render the chart', message, { showInTooltip: false });
            };
            GChartsDriver.prototype.draw = function (data, options) {
                console.log('Drawing with options ' + JSON.stringify(options));
                this.chart.draw(new this.chartModule.DataTable(data), options);
            };
            GChartsDriver.prototype.getStaticImage = function (callback) {
                if (this.chart.getImageURI) {
                    callback(this.chart.getImageURI());
                }
            };
            GChartsDriver.prototype.addChartReadyHandler = function (handler) {
                this.chartModule.events.addListener(this.chart, 'ready', handler);
            };
            GChartsDriver.prototype.addPageChangedHandler = function (handler) {
                this.chartModule.events.addListener(this.chart, 'page', function (e) {
                    handler(e.page);
                });
            };
            return GChartsDriver;
        }(ChartLibraryDriver));
        var Chart = /** @class */ (function () {
            function Chart(driver, dom, controlIds, base_options, refreshData, refreshInterval, totalRows) {
                this.driver = driver;
                this.dom = dom;
                this.controlIds = controlIds;
                this.base_options = base_options;
                this.refreshData = refreshData;
                this.refreshInterval = refreshInterval;
                this.totalRows = totalRows || -1; // Total rows in all (server-side) data.
                this.dataCache = {};
                this.optionsCache = {};
                this.hasIPython = false;
                try {
                    if (IPython) {
                        this.hasIPython = true;
                    }
                }
                catch (e) {
                }
                this.dom.innerHTML = '';
                this.removeStaticChart();
                this.addControls();
                // Generate and add a new static chart once chart is ready.
                var _this = this;
                this.driver.addChartReadyHandler(function () {
                    _this.addStaticChart();
                });
            }
            // Convert any string fields that are date type to JS Dates.
            Chart.convertDates = function (data) {
                for (var i = 0; i < data.cols.length; i++) {
                    if (data.cols[i].type == 'date' || data.cols[i].type == 'datetime') {
                        var rows = data.rows;
                        for (var j = 0; j < rows.length; j++) {
                            rows[j].c[i].v = new Date(rows[j].c[i].v);
                        }
                    }
                    else if (data.cols[i].type == 'timeofday') {
                        var rows = data.rows;
                        for (var j = 0; j < rows.length; j++) {
                            var timeInSeconds = rows[j].c[i].v.split('.')[0];
                            rows[j].c[i].v = timeInSeconds.split(':').map(function (n) {
                                return parseInt(n, 10);
                            });
                        }
                    }
                }
            };
            // Extend the properties in a 'base' object with the changes in an 'update' object.
            // We can add properties or override properties but not delete yet.
            Chart.extend = function (base, update) {
                for (var p in update) {
                    if (typeof base[p] !== 'object' || !base.hasOwnProperty(p)) {
                        base[p] = update[p];
                    }
                    else {
                        this.extend(base[p], update[p]);
                    }
                }
            };
            // Get the IPython cell associated with this chart.
            Chart.prototype.getCell = function () {
                if (!this.hasIPython) {
                    return undefined;
                }
                var cells = IPython.notebook.get_cells();
                for (var cellIndex in cells) {
                    var cell = cells[cellIndex];
                    if (cell.element && cell.element.length) {
                        var element = cell.element[0];
                        var chartDivs = element.getElementsByClassName('bqgc');
                        if (chartDivs && chartDivs.length) {
                            for (var i = 0; i < chartDivs.length; i++) {
                                if (chartDivs[i].id == this.dom.id) {
                                    return cell;
                                }
                            }
                        }
                    }
                }
                return undefined;
            };
            Chart.prototype.getRefreshHandler = function (useCache) {
                var _this = this;
                return function () {
                    _this.refresh(useCache);
                };
            };
            // Bind event handlers to the chart controls, if any.
            Chart.prototype.addControls = function () {
                if (!this.controlIds) {
                    return;
                }
                var controlHandler = this.getRefreshHandler(true);
                for (var i = 0; i < this.controlIds.length; i++) {
                    var id = this.controlIds[i];
                    var split = id.indexOf(':');
                    var control;
                    if (split >= 0) {
                        // Checkbox group.
                        var count = parseInt(id.substring(split + 1));
                        var base = id.substring(0, split + 1);
                        for (var j = 0; j < count; j++) {
                            control = document.getElementById(base + j);
                            control.disabled = !this.hasIPython;
                            control.addEventListener('change', function () {
                                controlHandler();
                            });
                        }
                        continue;
                    }
                    // See if we have an associated control that needs dual binding.
                    control = document.getElementById(id);
                    if (!control) {
                        // Kernel restart?
                        return;
                    }
                    control.disabled = !this.hasIPython;
                    var textControl = document.getElementById(id + '_value');
                    if (textControl) {
                        textControl.disabled = !this.hasIPython;
                        textControl.addEventListener('change', function () {
                            if (control.value != textControl.value) {
                                control.value = textControl.value;
                                controlHandler();
                            }
                        });
                        control.addEventListener('change', function () {
                            textControl.value = control.value;
                            controlHandler();
                        });
                    }
                    else {
                        control.addEventListener('change', function () {
                            controlHandler();
                        });
                    }
                }
            };
            // Iterate through any widget controls and build up a JSON representation
            // of their values that can be passed to the Python kernel as part of the
            // magic to fetch data (also used as part of the cache key).
            Chart.prototype.getControlSettings = function () {
                var env = {};
                if (this.controlIds) {
                    for (var i = 0; i < this.controlIds.length; i++) {
                        var id = this.controlIds[i];
                        var parts = id.split('__');
                        var varName = parts[1];
                        var splitPoint = varName.indexOf(':');
                        if (splitPoint >= 0) {
                            var count = parseInt(varName.substring(splitPoint + 1));
                            varName = varName.substring(0, splitPoint);
                            var cbBaseId = parts[0] + '__' + varName + ':';
                            var list = [];
                            env[varName] = list;
                            for (var j = 0; j < count; j++) {
                                var cb = document.getElementById(cbBaseId + j);
                                if (!cb) {
                                    // Stale refresh; user re-executed cell.
                                    return undefined;
                                }
                                if (cb.checked) {
                                    list.push(cb.value);
                                }
                            }
                        }
                        else {
                            var e = document.getElementById(id);
                            if (!e) {
                                // Stale refresh; user re-executed cell.
                                return undefined;
                            }
                            if (e && e.type == 'checkbox') {
                                // boolean
                                env[varName] = e.checked;
                            }
                            else {
                                // picker/slider/text
                                env[varName] = e.value;
                            }
                        }
                    }
                }
                return env;
            };
            // Get a string representation of the current environment - i.e. control settings and
            // refresh data. This is used as a cache key.
            Chart.prototype.getEnvironment = function () {
                var controls = this.getControlSettings();
                if (controls == undefined) {
                    // This means the user has re-executed the cell and our controls are gone.
                    return undefined;
                }
                var env = { controls: controls };
                Chart.extend(env, this.refreshData);
                return JSON.stringify(env);
            };
            Chart.prototype.refresh = function (useCache) {
                // TODO(gram): remember last cache key and don't redraw chart if cache
                // key is the same unless this is an ML key and the number of data points has changed.
                this.removeStaticChart();
                var env = this.getEnvironment();
                if (env == undefined) {
                    // This means the user has re-executed the cell and our controls are gone.
                    console.log('No chart control environment; abandoning refresh');
                    return;
                }
                if (useCache && env in this.dataCache) {
                    this.draw(this.dataCache[env], this.optionsCache[env]);
                    return;
                }
                var code = '%_get_chart_data\n' + env;
                // TODO: hook into the notebook UI to enable/disable 'Running...' while we fetch more data.
                if (!this.cellElement) {
                    var cell = this.getCell();
                    if (cell && cell.element && cell.element.length == 1) {
                        this.cellElement = cell.element[0];
                    }
                }
                // Start the cell spinner in the notebook UI.
                if (this.cellElement) {
                    this.cellElement.classList.remove('completed');
                }
                var _this = this;
                datalab.session.execute(code, function (error, response) {
                    _this.handleNewData(env, error, response);
                });
            };
            Chart.prototype.handleNewData = function (env, error, response) {
                var data = response.data;
                // Stop the cell spinner in the notebook UI.
                if (this.cellElement) {
                    this.cellElement.classList.add('completed');
                }
                if (data == undefined || data.cols == undefined) {
                    error = 'No data';
                }
                if (error) {
                    this.driver.error(error);
                    return;
                }
                this.refreshInterval = response.refresh_interval;
                if (this.refreshInterval == 0) {
                    console.log('No more refreshes for ' + this.refreshData.name);
                }
                Chart.convertDates(data);
                var options = this.base_options;
                if (response.options) {
                    // update any options. We need to make a copy so we don't break the base options.
                    options = JSON.parse(JSON.stringify(options));
                    Chart.extend(options, response.options);
                }
                // Don't update or keep refreshing this if control settings have changed.
                var newEnv = this.getEnvironment();
                if (env == newEnv) {
                    console.log('Got refresh for ' + this.refreshData.name + ', ' + env);
                    this.draw(data, options);
                }
                else {
                    console.log('Stopping refresh for ' + env + ' as controls are now ' + newEnv);
                }
            };
            // Remove a static chart (PNG) from the notebook and the DOM.
            Chart.prototype.removeStaticChart = function () {
                var cell = this.getCell();
                if (cell) {
                    var pngDivs = cell.element[0].getElementsByClassName('output_png');
                    if (pngDivs) {
                        for (var i = 0; i < pngDivs.length; i++) {
                            pngDivs[i].innerHTML = '';
                        }
                    }
                    var cell_outputs = cell.output_area.outputs;
                    var changed = true;
                    while (changed) {
                        changed = false;
                        for (var outputIndex in cell_outputs) {
                            var output = cell_outputs[outputIndex];
                            if (output.output_type == 'display_data' && output.metadata.source_id == this.dom.id) {
                                cell_outputs.splice(outputIndex, 1);
                                changed = true;
                                break;
                            }
                        }
                    }
                }
                else {
                    // Not running under IPython; use a different approach and just clear the DOM.
                    // Iterate through the IPython outputs...
                    var outputDivs = document.getElementsByClassName('output_wrapper');
                    if (outputDivs) {
                        for (var i = 0; i < outputDivs.length; i++) {
                            // ...and any chart outputs in each...
                            var outputDiv = outputDivs[i];
                            var chartDivs = outputDiv.getElementsByClassName('bqgc');
                            if (chartDivs) {
                                for (var j = 0; j < chartDivs.length; j++) {
                                    // ...until we find the chart div ID we want...
                                    if (chartDivs[j].id == this.dom.id) {
                                        // ...then get any PNG outputs in that same output group...
                                        var pngDivs = outputDiv.
                                            getElementsByClassName('output_png');
                                        if (pngDivs) {
                                            for (var k = 0; k < pngDivs.length; k++) {
                                                // ... and clear their contents.
                                                pngDivs[k].innerHTML = '';
                                            }
                                        }
                                        return;
                                    }
                                }
                            }
                        }
                    }
                }
            };
            // Add a static chart (PNG) to the notebook. The notebook will in turn add it to the DOM when
            // the notebook is opened.
            Chart.prototype.addStaticChart = function () {
                var _this = this;
                this.driver.getStaticImage(function (img) {
                    _this.handleStaticChart(img);
                });
            };
            Chart.prototype.handleStaticChart = function (img) {
                if (img) {
                    var cell = this.getCell();
                    if (cell) {
                        var encoding = img.substr(img.indexOf(',') + 1); // strip leading base64 etc.
                        var static_output = {
                            metadata: {
                                source_id: this.dom.id
                            },
                            data: {
                                'image/png': encoding
                            },
                            output_type: 'display_data'
                        };
                        cell.output_area.outputs.push(static_output);
                    }
                }
            };
            // Set up a refresh callback if we have a non-zero interval and the DOM element still exists
            // (i.e. output hasn't been cleared).
            Chart.prototype.configureRefresh = function (refreshInterval) {
                if (refreshInterval > 0 && document.getElementById(this.dom.id)) {
                    window.setTimeout(this.getRefreshHandler(false), 1000 * refreshInterval);
                }
            };
            // Cache the current data and options and draw the chart.
            Chart.prototype.draw = function (data, options) {
                var env = this.getEnvironment();
                this.dataCache[env] = data;
                this.optionsCache[env] = options;
                if ('cols' in data) {
                    this.driver.draw(data, options);
                }
                this.configureRefresh(this.refreshInterval);
            };
            return Chart;
        }());
        //-----------------------------------------------------------
        // A special version of Chart for supporting paginated data.
        var PagedTable = /** @class */ (function (_super) {
            __extends(PagedTable, _super);
            function PagedTable(driver, dom, controlIds, base_options, refreshData, refreshInterval, totalRows) {
                var _this = _super.call(this, driver, dom, controlIds, base_options, refreshData, refreshInterval, totalRows) || this;
                _this.firstRow = 0; // Index of first row being displayed in page.
                _this.pageSize = base_options.pageSize || 25;
                if (_this.base_options.showRowNumber == undefined) {
                    _this.base_options.showRowNumber = true;
                }
                _this.base_options.sort = 'disable';
                var __this = _this;
                _this.driver.addPageChangedHandler(function (page) {
                    __this.handlePageEvent(page);
                });
                return _this;
            }
            // Get control settings for cache key. For paged table we add the first row offset of the table.
            PagedTable.prototype.getControlSettings = function () {
                var env = _super.prototype.getControlSettings.call(this);
                if (env) {
                    env.first = this.firstRow;
                }
                return env;
            };
            PagedTable.prototype.draw = function (data, options) {
                var count = this.pageSize;
                options.firstRowNumber = this.firstRow + 1;
                options.page = 'event';
                if (this.totalRows < 0) {
                    // We don't know where the end is, so we should have 'next' button.
                    options.pagingButtonsConfiguration = this.firstRow > 0 ? 'both' : 'next';
                }
                else {
                    count = this.totalRows - this.firstRow;
                    if (count > this.pageSize) {
                        count = this.pageSize;
                    }
                    if (this.firstRow + count < this.totalRows) {
                        // We are not on last page, so we should have 'next' button.
                        options.pagingButtonsConfiguration = this.firstRow > 0 ? 'both' : 'next';
                    }
                    else {
                        // We are on last page
                        if (this.firstRow == 0) {
                            options.pagingButtonsConfiguration = 'none';
                            options.page = 'disable';
                        }
                        else {
                            options.pagingButtonsConfiguration = 'prev';
                        }
                    }
                }
                _super.prototype.draw.call(this, data, options);
            };
            // Handle page forward/back events. Page will only be 0 or 1.
            PagedTable.prototype.handlePageEvent = function (page) {
                var offset = (page == 0) ? -1 : 1;
                this.firstRow += offset * this.pageSize;
                this.refreshData.first = this.firstRow;
                this.refreshData.count = this.pageSize;
                this.refresh(true);
            };
            return PagedTable;
        }(Chart));
        function convertListToDataTable(data) {
            if (!data || !data.length) {
                return { cols: [], rows: [] };
            }
            var firstItem = data[0];
            var names = Object.keys(firstItem);
            var columns = names.map(function (name) {
                return { id: name, label: name, type: typeof firstItem[name] };
            });
            var rows = data.map(function (item) {
                var cells = names.map(function (name) {
                    return { v: item[name] };
                });
                return { c: cells };
            });
            return { cols: columns, rows: rows };
        }
        // The main render method, called from render() wrapper below. dom is the DOM element
        // for the chart, model is a set of parameters from Python, and options is a JSON
        // set of options provided by the user in the cell magic body, which takes precedence over
        // model. An initial set of data can be passed in as a final optional parameter.
        function _render(driver, dom, chartStyle, controlIds, data, options, refreshData, refreshInterval, totalRows) {
            require(["base/js/namespace"], function (Jupyter) {
                var url = "datalab/";
                require(driver.requires(url, chartStyle), function () {
                    // chart module should be last dependency in require() call...
                    var chartModule = arguments[arguments.length - 1]; // See if it needs to be a member.
                    driver.init(chartModule);
                    options = options || {};
                    var chart;
                    if (chartStyle == 'paged_table') {
                        chart = new PagedTable(driver, dom, controlIds, options, refreshData, refreshInterval, totalRows);
                    }
                    else {
                        chart = new Chart(driver, dom, controlIds, options, refreshData, refreshInterval, totalRows);
                    }
                    Chart.convertDates(data);
                    chart.draw(data, options);
                    // Do we need to do anything to prevent it getting GCed?
                });
            });
        }
        function render(driverName, dom, events, chartStyle, controlIds, data, options, refreshData, refreshInterval, totalRows) {
            // If this is HTML from nbconvert we can't support paging so add some text making this clear.
            if (chartStyle == 'paged_table' && document.hasOwnProperty('_in_nbconverted')) {
                chartStyle = 'table';
                var p = document.createElement("div");
                p.innerHTML = '<br>(Truncated to first page of results)';
                dom.parentNode.insertBefore(p, dom.nextSibling);
            }
            // Allocate an appropriate driver.
            var driver;
            if (driverName == 'plotly') {
                driver = new PlotlyDriver(dom, chartStyle);
            }
            else if (driverName == 'gcharts') {
                driver = new GChartsDriver(dom, chartStyle);
            }
            else {
                throw new Error('Unsupported chart driver ' + driverName);
            }
            // Get data in form needed for GCharts.
            // We shouldn't need this; should be handled by caller.
            if (!data.cols && !data.rows) {
                data = this.convertListToDataTable(data);
            }
            // If we have a datalab session, we can go ahead and draw the chart; if not, add code to do the
            // drawing to an event handler for when the kernel is ready.
            if (IPython.notebook.kernel.is_connected()) {
                _render(driver, dom, chartStyle, controlIds, data, options, refreshData, refreshInterval, totalRows);
            }
            else {
                // If the kernel is not connected, wait for the event.
                events.on('kernel_ready.Kernel', function (e) {
                    _render(driver, dom, chartStyle, controlIds, data, options, refreshData, refreshInterval, totalRows);
                });
            }
        }
        Charting.render = render;
    })(Charting || (Charting = {}));
    return Charting;
});
