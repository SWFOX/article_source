<?php 

/**
 * User: qiming.c <qiming.c@foxmail.com>
 * Date: 2016/9/6
 * Time: 20:46
 */

include './FileCache.php';

class MySession
{
    protected $mySessionID;
    protected $sessionVal;
    protected $fileCache;

    public function __construct()
    {
        //获取传过来的 Cookie 中是否有 mySessionId,没有就随机生成
        if (isset($_COOKIE['mySessionId'])) {
            $this->mySessionID = $_COOKIE['mySessionId'];
        } else {
            $this->mySessionID = md5(substr(md5(time()), rand(1,10), rand(1,10)));
        }
        $this->fileCache = new FileCache();
        $this->sessionVal  = $this->fileCache->get($this->mySessionID) ? $this->fileCache->get($this->mySessionID) : array();
    }

    public function set($key, $val)
    {
        $this->sessionVal[$key] = $val;
    }

    public function get($key)
    {
        if (isset($this->sessionVal[$key])) {
            return $this->sessionVal[$key];
        }
        return null;
    }

    /** 保存值，发送 Cookie 报头 */
    public function save()
    {
        $this->fileCache->set($this->mySessionID, $this->sessionVal);
        header('Set-Cookie: mySessionId=' . $this->mySessionID . ';', false);
    }
}