<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
 
// files needed to connect to database
include_once 'config/database.php';
include_once 'objects/user.php';
include_once 'aux_functions/post_request.php';
 
// get database connection
$database = new Database();
$db = $database->getConnection();
 
// instantiate user object
$user = new User($db);

// get posted data
$data = json_decode(file_get_contents("php://input"));
 
//get request public ip and country code
$public_ip = $_SERVER['REMOTE_ADDR'];
$public_ip = strval($public_ip);
$country = post_request('http://ip-api.com/json/'.$public_ip.'?fields=countryCode', False, $content_type='json');
$country = ($country) ? $country : 'XX';


// set user property values
$user->username = $data->username;
$user->pswd = $data->pswd;
$user->public_ip = $public_ip;
$user->country = $country;

// create the user
if(
    !empty($user->username) &&
    !empty($user->pswd) &&
    !empty($user->public_ip) &&
    $user->create()
){
 
    // set response code
    http_response_code(200);
 
    // display message: user was created
    echo json_encode(array("message" => "User was created."));
}
 
// message if unable to create user
else{

    // set response code
    http_response_code(400);
 
    // display message: unable to create user
    echo json_encode(array("message" => "Unable to create user."));
}
