<?php
use dokuwiki\Utf8\Sort;

/**
 * Cgserver authentication backend
 *
 * @author     Tailing Yuan <yuantailing@gmail.com>
 */
class auth_plugin_authcgserver extends DokuWiki_Auth_Plugin
{
    public function __construct()
    {
        parent::__construct();
    }

    public function checkPass($user, $pass)
    {
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, array(
            'username' => $user,
            'password' => $pass,
            'ip' => $_SERVER['REMOTE_ADDR'],
            'client' => 'dokuwiki',
            'api_secret' => getenv('CGSERVER_API_SECRET'),
        ));
        curl_setopt($curl, CURLOPT_URL, 'http://cgserver/serverlist/opencheckuser');
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $response = curl_exec($curl);
        if (200 != curl_getinfo($curl, CURLINFO_HTTP_CODE)) {
            msg('Cgserver API error.');
            return false;
        }
        $response = json_decode($response, true);
        if ($response["error"] != 0) {
            msg($response["msg"]);
            return false;
        } else {
            return true;
        }
    }

    public function getUserData($user, $requireGroups = true)
    {
        return array(
            'name' => $user,
            'mail' => '',
            'grps' => array('cgserver'),
        );
    }
}
