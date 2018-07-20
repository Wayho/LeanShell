var express = require('express');
var router = express.Router();

var OAuth = require('wechat-oauth');

var config = {
    wechat:{
        appID:process.env.wechat_appID,
        appSecret:process.env.wechat_appsecret,
        token:process.env.wechat_token
    }
};

var client = new OAuth(config.wechat.appID, config.wechat.appSecret);

/* GET users listing. */
router.get('/', function (req, res, next) {
    var domain = "https://ssjk.leanapp.cn"
    var auth_callback_url = domain + "/oauth/callback"
    //var url = client.getAuthorizeURL(auth_callback_url, '', 'snsapi_userinfo');
    var url = client.getAuthorizeURL(auth_callback_url, '', 'snsapi_base');
    console.log(url);
    // 重定向请求到微信服务器
    res.redirect(url);
    console.log('redirect end');
});

router.get('/callback', function (req, res, next) {
    var code = req.query.code;
    client.getAccessToken(code, function (err, result) {
        console.log(result)
        var accessToken = result.data.access_token;
        var openid = result.data.openid;

        client.getUser(openid, function (err, result) {
            var userInfo = result;
            // save or other opration
            res.json(userInfo)
        });
    });
});

module.exports = router;
