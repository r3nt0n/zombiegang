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
include_once 'objects/task.php';
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

        // instantiate object
        $task = new Task($db);
        
        // check who request and permissions
        $requested_by = $decoded->data->username;

        if (is_zombie($db, $requested_by)){
            $zombie_view = True;
            $by_id = (isset($data->id)) ? $data->id : "";
            $mission_id = (isset($data->mission_id)) ? $data->mission_id : "";
            $by_submit_at_bef =  False;
            $by_submit_at_aft = False;
            $by_master_username = False;
            if (!$by_id or !$mission_id) {
                throw new Exception('Not id provided');
            }
            else {
                $mission = new Mission($db);
                $mission->id = $mission_id;
                $mission->task_id = $by_id;
                $mission->zombie_username = $requested_by;
                if (!$mission->idExists()){
                    throw new Exception('Zombie trying to read a task which isnt assigned to him');
                }
            }
        }
        
        else{
            $zombie_view = False;
            // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
            //check_master_permissions($requested_by);
            // set filters by request (only if requested by master)
            $by_master_username =  $requested_by;
            $by_submit_at_bef = (isset($data->submit_at_bef)) ? $data->submit_at_bef : "";
            $by_submit_at_aft = (isset($data->submit_at_aft)) ? $data->submit_at_aft : "";
            $by_task_type = (isset($data->task_type)) ? $data->task_type : "";
        }
        
        
        
        // retrieve records
        $tasks_data = $task->read($by_id, $by_master_username, $by_submit_at_bef, $by_submit_at_aft, 
                                  $by_task_type, $zombie_view);

        
        if ($tasks_data) {
            for ($i=0; $i < count($tasks_data); $i++) { 
                $tasks_data[$i]["task_content"] = json_decode(decrypt($tasks_data[$i]["task_content"], $key));
            }
        }
            

        if($tasks_data){
            
            // set response code
            http_response_code(200);
            
            // response in json format
            echo json_encode($tasks_data);
        }
        
        // message if unable to update user
        else{
            // set response code
            http_response_code(204);
        
            // show error message
            echo json_encode(array("message" => "Any task found."));
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