<?php
/**
 * 发送curl请求
 */
class WeiXinClient {
    function submit($url, $data, $cookie = false) {
        return $this->exec($url, $data, $cookie);
    }

    function get($url, $cookie) {
        return $this->exec($url, false, $cookie, false);
    }

    /**
     * 返回array(cookie=>, body=>)
     * @param  [type] $url    [description]
     * @param  [array] $data   [description]
     * @param  [type] $cookie [description]
     * @return [type]         [description]
     */
    private function exec($url, $data, $cookie = false, $isPost = true) {
        $dataStr = "";
	$dataStr = $data;

        $curl = curl_init($url); // 启动一个CURL会话
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0); // 对认证证书来源的检查
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2); // 从证书中检查SSL加密算法是否存在
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1); // 使用自动跳转
	curl_setopt($curl, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Content-Length: ' . strlen($dataStr)));

        if($isPost) {
	    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "POST");
            curl_setopt($curl, CURLOPT_POSTFIELDS, $dataStr); // Post提交的数据包
        }

        curl_setopt($curl, CURLOPT_TIMEOUT, 30); // 设置超时限制防止死循环
        curl_setopt($curl, CURLOPT_HEADER, 1); // 显示返回的Header区域内容
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true); // 获取的信息以文件流的形式返回

        if($cookie) {
            curl_setopt($curl, CURLOPT_COOKIE, $cookie);
        }

        $tmpInfo = curl_exec($curl); // 执行操作
        if (curl_errno($curl)) {
           echo 'Errno'. curl_error($curl);//捕抓异常

           return;
        }

        curl_close($curl); // 关闭CURL会话

        // 解析HTTP数据流
        list($header, $body) = explode("\r\n\r\n", $tmpInfo, 2);

        if(!$cookie) {
            // 解析COOKIE
            $cookie = "";
            preg_match_all("/set\-cookie: (.*)/i", $header, $matches);
            if(count($matches == 2)) {
                foreach($matches[1] as $each) {
                    $cookie .= trim($each). ";";
                }
            }
        }

        return array("cookie" => $cookie, "body" => trim($body));
    }
}
