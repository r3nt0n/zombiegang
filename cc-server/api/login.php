<?php
// required headers
//header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
 
// files needed to connect to database
include_once 'config/database.php';
include_once 'objects/user.php';
include_once 'util/check_permission.php';
include_once 'create_access_log.php';
include_once 'util/post_request.php';
 
// get database connection
$database = new Database();
$db = $database->getConnection();
 
// instantiate user object
$user = new User($db);
 
// get posted data
$data = json_decode(file_get_contents("php://input"));

//print_r(file_get_contents("php://input"));
 
// set product property values
$user->username = $data->username;
$username_exists = $user->usernameExists();

// generate json web token
include_once 'config/core.php';
include_once 'libs/php-jwt/src/BeforeValidException.php';
include_once 'libs/php-jwt/src/ExpiredException.php';
include_once 'libs/php-jwt/src/SignatureInvalidException.php';
include_once 'libs/php-jwt/src/JWT.php';
use \Firebase\JWT\JWT;
 
$successful = 0;
// check if username exists and if password is correct
// var_dump($username_exists);
// var_dump(password_verify($data->pswd, $user->pswd));
// var_dump($data->pswd);
// var_dump($user->pswd);
if($username_exists && password_verify($data->pswd, $user->pswd)){

    $successful = 1;
    $token = array(
       "iat" => $issued_at,
       "exp" => $expiration_time,
       "iss" => $issuer,
       "data" => array(
           //"id" => $user->id,
           "username" => $user->username
       )
    );
 
    // set response code
    http_response_code(200);
 
    // generate jwt
    $jwt = JWT::encode($token, $key, 'HS256');
    echo json_encode(
            array(
                "message" => "Successful login.",
                "jwt" => $jwt
            )
        );
 
}
 
// login failed
else{
    // set response code
    http_response_code(401);
 
    // tell the user login failed
    echo json_encode(array("message" => "Login failed."));
}

//$public_ip = ($_SERVER['REMOTE_ADDR'] == ': : 1') ? '127.0.0.1' : $_SERVER['REMOTE_ADDR'] ;
$public_ip = $_SERVER['REMOTE_ADDR'];
$public_ip = strval($public_ip);
$country = post_request('http://ip-api.com/json/'.$public_ip.'?fields=countryCode', False, $content_type='json');
$country = ($country) ? $country : 'XX';
//$public_ip = '127.0.0.1';

// create access log

// !! FALTA COMPROBAR SI ES MASTER, EN ESE CASO NO CREAR REGISTRO DE LOGIN

$log_data = array("successful" => $successful,
                  "username" => $data->username,
                  "public_ip" => $public_ip,
                  "country" => $country,
                  "hostname" => $data->hostname);

if ($store_masters_acess_logs or !(is_master($db, $user->username))) {
    create_access_log($log_data);
}

?>
