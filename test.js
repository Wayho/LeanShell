var OAuth = require('wechat-oauth');
var auth = new OAuth('wx76cc8ae402a1c613', 'd9ccfdbc8cb5a75956f97d854fd0a09b');
var url = auth.getAuthorizeURL('http://sale.leanapp.cn/', 'hehe', 'snsapi_userinfo');
console.log('auth.getAuthorizeURL():', url);
