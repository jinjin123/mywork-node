<?php
require($G_ROOT. "/include/WeiXinClient.php");

class WeiXin
{
	private $corpid;
	private $corpsecret;
	private $agentid;
	private $access_token;

	private $wx;
	private $cookie;

        // 构造函数
        public function __construct($config) {
                if(!$config) {
                        exit("error");
                }

                // 配置初始化
                $this->corpid = $config['CorpID'];
                $this->corpsecret = $config['Secret'];
		$this->agentid = $config['agentid'];

                $this->wx = new WeiXinClient();

		// 读取Token
		$this->login();
        }

	/*
	* 获取access_token
	Https请求方式: GET
	https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=id&corpsecret=secrect
	参数		必须	说明
	corpid		是	企业Id
	corpsecret	是	管理组的凭证密钥
	Json返回结果:
	{
   		"access_token": "accesstoken000001",
   		"expires_in": 7200
	}
	*/
	public function login() {
		$url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={$this->corpid}&corpsecret={$this->corpsecret}";
		$re = $this->wx->get($url, $this->cookie);
		$body = json_decode($re['body'], true);		
		$this->access_token = $body['access_token'];
	}

	/*
	* 发送文本消息
	Https请求方式: POST
	地址: https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
	参数	必须	说明
	touser	否	成员ID列表（消息接收者，多个接收者用 | 分隔，最多支持1000个。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
	toparty	否	部门ID列表，多个接收者用 | 分隔，最多支持100个。当touser为@all时忽略本参数
	totag	否	标签ID列表，多个接收者用 | 分隔。当touser为@all时忽略本参数
	msgtype	是	消息类型，此时固定为：text
	agentid	是	企业应用的id，整型。可在应用的设置页面查看
	content	是	消息内容
	safe	否	表示是否是保密消息，0表示否，1表示是，默认0
	*/
	public function send($usr = NULL, $dep = NULL, $tag = NULL, $content)
	{
		$post = array();
		$post['msgtype'] = 'text';
		$post['agentid'] = $this->agentid;
		$post['safe'] = '0';
		$post['text']['content'] = $content;
		$post['touser'] = $usr;
		$post['toparty'] = $dep;
		$post['totag'] = $tag;
		$url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={$this->access_token}";
		$re = $this->wx->submit($url, json_encode($post,JSON_UNESCAPED_UNICODE), $this->cookie);
		return json_decode($re['body']);
	}
}
