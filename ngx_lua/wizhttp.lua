local zhttp = require "resty.http"
local cjson = require "cjson"
local function http_post_client(url, timeout)
        local httpc = zhttp.new()

        timeout = timeout or 30000
        httpc:set_timeout(timeout)

        local res, err_ = httpc:request_uri(url, {
                method = "GET",
                headers = {
                    ["Content-Type"] = "application/json";
                }
        })
        httpc:set_keepalive(5000, 100)
        --httpc:close()
        return res, err_
end
local resp, err = http_post_client("http://192.168.50.100:82/as/oauth/token?clientId=g8kkcxf2&clientSecret=dkrmy6rfu95k1cziogzqoo4t",3000)
--ngx.say(resp.body)
local json = cjson.decode(resp.body)

local res,err = http_post_client("http://192.168.50.100:82/as/oauth/service/login_url?accessToken="..json.result.accessToken.."&userId=reader@qq.com",3000)
--ngx.say(res.body)
local red = cjson.decode(res.body)
return ngx.redirect(red.result,301)
