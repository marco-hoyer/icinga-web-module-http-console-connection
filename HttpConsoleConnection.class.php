<?php

class HttpConsoleConnection extends BaseConsoleConnection {

        private $host = null;
        private $port = 8080;
        private $username = null;
        private $password = null;
        private $authType = "none";

        public function exec(Api_Console_ConsoleCommandModel $cmd) {
                $cmdString = "";
                // get arguments from ConsoleCommand
                $args = $cmd->getArguments();

                foreach($args as $name => $arg) {
                        // args are formatted as following: [1376055378] SCHEDULE_HOST_CHECK;devica01;1376062577, we dont need the timestamp
                        $value = explode(" ", $arg, 2);
                        if ($value[1] != '') {
                                // append the cleaned arg to cmdString
                                $cmdString .= $value[1];
                        }
                }
                // build url for livestatus-service to send http-get with query
                $url = "http://" . $this->host . ":" . $this->port . "/cmd?q=" . urlencode($cmdString) . "&handler=icinga";
                // get http statuscode, it is 0, if there was a connection problem f.e.
                $httpCode = $this->SendRequestByHttpGet($url);
                if($httpCode == 200) {
                        // everything is fine, the command has been queued into icinga.cmd on target host
                        $cmd->setReturnCode(0);
                } else {
                        $cmd->setReturnCode($httpCode);
                }
        }

        function SendRequestByHttpGet($url) {
                $connection = curl_init($url);
                curl_setopt($connection, CURLOPT_HTTPHEADER, array('Content-Type: application/xml'));
                curl_setopt($connection, CURLOPT_HEADER, 1);
                curl_setopt($connection, CURLOPT_TIMEOUT, 30);
                curl_setopt($connection, CURLOPT_RETURNTRANSFER, TRUE);
                curl_setopt($connection, CURLOPT_USERAGENT,"icinga-web");
                // if configured, apply username and passwort for basic auth
                if ($this->authType = 'password') {
                        curl_setopt($connection,CURLOPT_USERPWD,"$this->username:$this->password");
                }

                $return = curl_exec($connection);
                $httpCode = curl_getinfo($connection, CURLINFO_HTTP_CODE);
                curl_close($connection);
                return $httpCode;
        }

        public function __construct(array $settings = array()) {
                $settings = $settings["auth"];
                // get hostname and auth type (none | basic)
                $this->host = $settings["host"];
                $this->port = $settings["port"];
                $this->authType = $settings["method"];
                $this->setupAuth($settings);
        }

        protected function setupAuth(array $settings) {
                switch ($this->authType) {
                        case 'none':
                                $this->username = $settings["user"];
                                break;

                        case 'password':
                                $this->password = $settings["password"];
                                $this->username = $settings["user"];
                                break;

                        default:
                                throw new ApiInvalidAuthTypeException("Unknown auth type ".$this->authType);
                }
        }

}
