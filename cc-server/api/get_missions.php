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
include_once 'objects/mission.php';

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

        // get database connection
        $database = new Database();
        $db = $database->getConnection();
        
        // check who request and permissions
        $requested_by = $decoded->data->username;

        if (is_zombie($db, $requested_by)){
            $zombie_view = True;
            $by_id = (isset($data->id)) ? $data->id : "";
            $by_task_id = (isset($data->task_id)) ? $data->task_id : "";
            $by_read_confirm = (isset($data->read_confirm)) ? $data->read_confirm : "";
            $by_zombie_username =  $requested_by;
            $by_created_bef =  "";
            $by_created_aft = "";
        }
        
        else{
            $zombie_view = False;
            // this function raise exceptions in case of error (not requested by a zombie, or requesting changes on another zombie)
            check_master_permissions($requested_by);
            // set filters by request (only if requested by zombie)
            $by_id = (isset($data->id)) ? $data->id : "";
            $by_task_id = (isset($data->task_id)) ? $data->task_id : "";
            $by_read_confirm = (isset($data->read_confirm)) ? $data->read_confirm : "";
            $by_zombie_username = (isset($data->zombie_username)) ? $data->zombie_username : "";
            $by_created_bef = (isset($data->created_bef)) ? $data->created_bef : "";
            $by_created_aft = (isset($data->created_aft)) ? $data->created_aft : "";
            
        }
        
        // instantiate user object
        $mission = new Mission($db);
        
        // retrieve records
        $missions_data = $mission->read($by_id, $by_task_id, $by_read_confirm, $by_zombie_username, $by_created_bef, $by_created_aft, 
                                        $zombie_view=$zombie_view);

        
        // for ($i=0; $i < count($missions_data); $i++) { 
        //     $missions_data[$i]["mission_content"] = json_decode(decrypt($missions_data[$i]["mission_content"], $key));
        // }
            

        if($missions_data){
            
            // set response code
            http_response_code(200);
            
            // response in json format
            echo json_encode($missions_data);
        }
        
        // message if unable to update user
        else{
            // set response code
            http_response_code(202);
        
            // show error message
            echo json_encode(array("message" => "Any mission found."));
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