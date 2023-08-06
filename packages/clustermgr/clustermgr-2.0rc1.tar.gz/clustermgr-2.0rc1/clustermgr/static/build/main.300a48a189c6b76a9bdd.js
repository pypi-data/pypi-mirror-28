webpackJsonp([1],{

/***/ 24:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(4);

var _react2 = _interopRequireDefault(_react);

var _reactDom = __webpack_require__(12);

var _reactDom2 = _interopRequireDefault(_reactDom);

var _axios = __webpack_require__(18);

var _axios2 = _interopRequireDefault(_axios);

var _logitem = __webpack_require__(58);

var _logitem2 = _interopRequireDefault(_logitem);

var _messageitem = __webpack_require__(59);

var _messageitem2 = _interopRequireDefault(_messageitem);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var LogContainer = function (_Component) {
    _inherits(LogContainer, _Component);

    function LogContainer(props) {
        _classCallCheck(this, LogContainer);

        var _this = _possibleConstructorReturn(this, (LogContainer.__proto__ || Object.getPrototypeOf(LogContainer)).call(this, props));

        _this.state = {
            items: _this.props.items
        };
        return _this;
    }

    _createClass(LogContainer, [{
        key: "scrollToBottom",
        value: function scrollToBottom() {
            var node = _reactDom2.default.findDOMNode(this.logEnd);
            node.scrollIntoView({ behavior: "smooth" });
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.scrollToBottom();
        }
    }, {
        key: "componentDidUpdate",
        value: function componentDidUpdate() {
            this.scrollToBottom();
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            var msgItems = this.props.items.map(function (itemInfo) {
                if (itemInfo.hasOwnProperty('output') && itemInfo.hasOwnProperty('action')) {
                    var id = itemInfo.id,
                        action = itemInfo.action,
                        state = itemInfo.state,
                        output = itemInfo.output;

                    return _react2.default.createElement(_logitem2.default, {
                        key: id,
                        id: id,
                        action: action,
                        state: state,
                        output: output,
                        server: _this2.props.server
                    });
                } else {
                    // TODO pass the the individual properties instead of itemInfo object
                    return _react2.default.createElement(_messageitem2.default, {
                        key: Math.random(),
                        level: itemInfo.level,
                        msg: itemInfo.msg
                    });
                }
            });

            return _react2.default.createElement(
                "div",
                { className: this.props.show ? "log-body" : "hidden" },
                msgItems,
                _react2.default.createElement("div", { style: { float: "left", clear: "both" }, ref: function ref(el) {
                        _this2.logEnd = el;
                    } })
            );
        }
    }]);

    return LogContainer;
}(_react.Component);

var Logger = function (_Component2) {
    _inherits(Logger, _Component2);

    function Logger(props) {
        _classCallCheck(this, Logger);

        var _this3 = _possibleConstructorReturn(this, (Logger.__proto__ || Object.getPrototypeOf(Logger)).call(this, props));

        _this3.state = {
            logData: {
                messages: []
            },
            showContent: true
        };
        _this3.fetchData = _this3.fetchData.bind(_this3);
        _this3.toggleContentView = _this3.toggleContentView.bind(_this3);
        return _this3;
    }

    _createClass(Logger, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var _this4 = this;

            this.timerID = setInterval(function () {
                return _this4.fetchData();
            }, 500);
        }
    }, {
        key: "fetchData",
        value: function fetchData() {
            var _this5 = this;

            var id = document.clustermgr.task_id;
            _axios2.default.get("/log/" + id).then(function (response) {
                _this5.setState({ logData: response.data });
                if (response.data.state === 'SUCCESS' || response.data.state === 'FAILURE') {
                    clearInterval(_this5.timerID);
                }
            });
        }
    }, {
        key: "componentWillUnmount",
        value: function componentWillUnmount() {
            clearInterval(this.timerID);
        }
    }, {
        key: "toggleContentView",
        value: function toggleContentView() {
            this.setState(function (prevState) {
                return { showContent: !prevState.showContent };
            });
        }
    }, {
        key: "render",
        value: function render() {
            return _react2.default.createElement(
                "div",
                { className: "logger" },
                _react2.default.createElement(
                    "div",
                    { className: "row log-header" },
                    _react2.default.createElement("div", { className: "col-md-8" }),
                    _react2.default.createElement(
                        "div",
                        { className: "col-md-4" },
                        this.state.showContent ? _react2.default.createElement(
                            "button",
                            { className: "logger-button pull-right", onClick: this.toggleContentView },
                            _react2.default.createElement("i", { className: "glyphicon glyphicon-eye-close" }),
                            "  Hide Logs"
                        ) : _react2.default.createElement(
                            "button",
                            { className: "logger-button pull-right", onClick: this.toggleContentView },
                            _react2.default.createElement("i", { className: "glyphicon glyphicon-eye-open" }),
                            "  Show Logs"
                        )
                    )
                ),
                _react2.default.createElement(LogContainer, { items: this.state.logData.messages, show: this.state.showContent, server: "example.com" })
            );
        }
    }]);

    return Logger;
}(_react.Component);

_reactDom2.default.render(_react2.default.createElement(Logger, null), document.getElementById('log_root'));

/***/ }),

/***/ 58:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(4);

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var StateIcon = function StateIcon(props) {
    var state = props.state;

    if (state === 'running') {
        return _react2.default.createElement('i', { className: 'glyphicon glyphicon-flash text-warning' });
    } else if (state === 'fail') {
        return _react2.default.createElement('i', { className: 'glyphicon glyphicon-remove-circle text-danger' });
    } else if (state === 'success') {
        return _react2.default.createElement('i', { className: 'glyphicon glyphicon-ok-circle text-success' });
    } else if (state === 'complete') {
        return _react2.default.createElement('i', { className: 'glyphicon glyphicon-ok text-info' });
    }
    return state;
};

var LogItem = function (_Component) {
    _inherits(LogItem, _Component);

    function LogItem(props) {
        _classCallCheck(this, LogItem);

        var _this = _possibleConstructorReturn(this, (LogItem.__proto__ || Object.getPrototypeOf(LogItem)).call(this, props));

        _this.state = {
            outputShown: true
        };
        _this.toggleOutput = _this.toggleOutput.bind(_this);
        return _this;
    }

    _createClass(LogItem, [{
        key: 'toggleOutput',
        value: function toggleOutput() {
            this.setState(function (prevState) {
                return {
                    outputShown: !prevState.outputShown
                };
            });
        }
    }, {
        key: 'componentWillUpdate',
        value: function componentWillUpdate(prevProps) {
            if (prevProps.state !== this.props.state) {
                this.setState({ outputShown: false });
            }
        }
    }, {
        key: 'render',
        value: function render() {
            return _react2.default.createElement(
                'div',
                { id: "logItem_" + this.props.id, className: 'log-item' },
                _react2.default.createElement(
                    'div',
                    { className: 'row' },
                    _react2.default.createElement(
                        'div',
                        { className: 'col-md-10' },
                        _react2.default.createElement(
                            'p',
                            { className: "command command-" + this.props.state },
                            _react2.default.createElement(StateIcon, { state: this.props.state }),
                            _react2.default.createElement(
                                'span',
                                { className: 'host' },
                                ' root@',
                                this.props.server,
                                ':~# '
                            ),
                            this.props.action
                        )
                    ),
                    _react2.default.createElement(
                        'div',
                        { className: 'col-md-2', onClick: this.toggleOutput },
                        this.state.outputShown ? _react2.default.createElement(
                            'span',
                            { className: 'label label-default', style: { cursor: "pointer" } },
                            'hide log'
                        ) : _react2.default.createElement(
                            'span',
                            { className: 'label label-default', style: { cursor: "pointer" } },
                            'show log'
                        )
                    )
                ),
                _react2.default.createElement(
                    'pre',
                    { id: "pre_" + this.props.id, className: this.state.outputShown ? "" : "hidden" },
                    this.props.output
                )
            );
        }
    }]);

    return LogItem;
}(_react.Component);

exports.default = LogItem;

/***/ }),

/***/ 59:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _react = __webpack_require__(4);

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var MsgIcon = function MsgIcon(props) {
    switch (props.level) {
        case "info":
            return _react2.default.createElement("i", { className: "glyphicon glyphicon-info-sign" });
        case "success":
            return _react2.default.createElement("i", { className: "glyphicon glyphicon-ok-sign" });
        case "warning":
            return _react2.default.createElement("i", { className: "glyphicon glyphicon-warning-sign" });
        case "danger":
        case "error":
        case "fail":
            return _react2.default.createElement("i", { className: "glyphicon glyphicon-remove-sign" });
        default:
            return _react2.default.createElement("i", { className: "glyphicon glyphicon-ok" });
    }
};

var Msg = function Msg(props) {
    return _react2.default.createElement(
        "p",
        { className: "msg msg-" + props.level },
        _react2.default.createElement(MsgIcon, { level: props.level }),
        " ",
        "  " + props.msg
    );
};

var MessageItem = function (_Component) {
    _inherits(MessageItem, _Component);

    function MessageItem(props) {
        _classCallCheck(this, MessageItem);

        return _possibleConstructorReturn(this, (MessageItem.__proto__ || Object.getPrototypeOf(MessageItem)).call(this, props));
    }

    _createClass(MessageItem, [{
        key: "render",
        value: function render() {
            var message = null;
            if (this.props.level === "debug") {
                message = _react2.default.createElement(
                    "pre",
                    null,
                    this.props.msg
                );
            } else {
                message = _react2.default.createElement(Msg, { level: this.props.level, msg: this.props.msg });
            }
            return _react2.default.createElement(
                "div",
                { className: "log-item" },
                message
            );
        }
    }]);

    return MessageItem;
}(_react.Component);

exports.default = MessageItem;

/***/ })

},[24]);