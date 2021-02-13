<?php

// show error reporting
error_reporting(E_ALL);
 
// set your default time-zone
date_default_timezone_set('Asia/Manila');
 
// variables used for jwt
$key = "example_ultra_secret_key";
$issued_at = time();
$expiration_time = $issued_at + (60 * 10); // valid for 10 minutes
$issuer = "http://localhost/zgang/RestApiAuthLevel1/";


// enable/disable store access logs for masters
$store_masters_acess_logs = True;
?>