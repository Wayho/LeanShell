'use strict';

var express = require('express');
var timeout = require('connect-timeout');
var path = require('path');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var AV = require('leanengine');

// 加载云函数定义，你可以将云函数拆分到多个文件方便管理，但需要在主文件中加载它们
require('./cloud');

var config = {
    wechat:{
        appID:"wx76cc8ae402a1c613",
        appSecret:"d9ccfdbc8cb5a75956f97d854fd0a09b",
        token:"mytest"
    }
};
var OAuth = require('wechat-oauth');
var oauth = new OAuth(config.wechat.appID, config.wechat.appSecret);

var app = express();

// 设置模板引擎
//app.set('view engine', 'ejs');

//app.use(express.static('public'));

// 设置默认超时时间
app.use(timeout('15s'));

// 加载云引擎中间件
app.use(AV.express());

app.enable('trust proxy');
// 需要重定向到 HTTPS 可去除下一行的注释。
// app.use(AV.Cloud.HttpsRedirect());

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());

app.get('/', function(req, res) {
    //res.render('index', { currentTime: new Date() });
    //return 'This is home page'
    var Token=config.wechat.token;
    var domain = "http://sale.leanapp.cn"
    var auth_callback_url = domain + "/oauth/callback"
    var url = oauth.getAuthorizeURL(auth_callback_url, '', 'snsapi_userinfo');
    console.log(url);
    // 重定向请求到微信服务器
    res.redirect(url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('This is home page');
});

app.get('/callback', function(req, res) {
    //res.render('index', { currentTime: new Date() });
    //return 'This is home page'
    var code = req.query.code;
    oauth.getAccessToken(code, function (err, result) {
        console.log(result)
        var accessToken = result.data.access_token;
        var openid = result.data.openid;

        oauth.getUser(openid, function (err, result) {
            var userInfo = result;
            // save or other opration
            res.json(userInfo)
        });
    });
});

app.use(function(req, res, next) {
  // 如果任何一个路由都没有返回响应，则抛出一个 404 异常给后续的异常处理器
  if (!res.headersSent) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
  }
});

// error handlers
app.use(function(err, req, res, next) {
    if (req.timedout && req.headers.upgrade === 'websocket') {
        // 忽略 websocket 的超时
        return;
    }

    var statusCode = err.status || 500;
        if (statusCode === 500) {
        console.error(err.stack || err);
    }
    if (req.timedout) {
        console.error('请求超时: url=%s, timeout=%d, 请确认方法执行耗时很长，或没有正确的 response 回调。', req.originalUrl, err.timeout);
        }
    res.status(statusCode);
    // 默认不输出异常详情
    var error = {};
    if (app.get('env') === 'development') {
        // 如果是开发环境，则将异常堆栈输出到页面，方便开发调试
        error = err;
    }
    //res.render('error', {
    //    message: err.message,
    //    error: error
    //});
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end(err.message);
});

module.exports = app;
