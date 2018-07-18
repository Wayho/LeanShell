'use strict';

var AV = require('leanengine');

var config = {
    wechat:{
        appID:"wx76cc8ae402a1c613",
        appSecret:"d9ccfdbc8cb5a75956f97d854fd0a09b",
        token:"mytest"
    }
};

var token=config.wechat.token;

AV.init({
  appId: process.env.LEANCLOUD_APP_ID,
  appKey: process.env.LEANCLOUD_APP_KEY,
  masterKey: process.env.LEANCLOUD_APP_MASTER_KEY
});

// 如果不希望使用 masterKey 权限，可以将下面一行删除
AV.Cloud.useMasterKey();

var app = require('./app');

// 端口一定要从环境变量 `LEANCLOUD_APP_PORT` 中获取。
// LeanEngine 运行时会分配端口并赋值到该变量。
var PORT = parseInt(process.env.LEANCLOUD_APP_PORT || process.env.PORT || 80);
console.log('PORT:', PORT);

console.log('process.env.LEANCLOUD_AVAILABLE_CPUS', process.env.LEANCLOUD_AVAILABLE_CPUS);

app.listen(PORT, function (err) {
  console.log('Node app is running on port:', PORT);

  // 注册全局未捕获异常处理器
  process.on('uncaughtException', function(err) {
    console.error('Caught exception:', err.stack);
  });
  process.on('unhandledRejection', function(reason, p) {
    console.error('Unhandled Rejection at: Promise ', p, ' reason: ', reason.stack);
  });
});
