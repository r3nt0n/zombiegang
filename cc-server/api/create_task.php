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
        // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
        check_master_permissions($requested_by);

        // get database connection
        $database = new Database();
        $db = $database->getConnection();
        
        // instantiate task object
        $task = new Task($db);
        
        // set task property values
        // light encryption of task content, not for security porpuses but to avoid strip any char when sanitize 
        // (commands and other text that could be included here as a task don't be sanitized but crypted when creating and decrypted at reading)
        // this way of "packing" also allow to store in db nested data as a unique field
        $task->task_content = (isset($data->task_content)) ? encrypt(json_encode($data->task_content), $key) : "";
        $task->task_name = $data->task_name;
        $task->task_type = $data->task_type;
        $task->master_username = $requested_by;
        $task->to_exec_at = $data->to_exec_at;
        $task->to_stop_at = $data->to_stop_at;
        $task->manual_stop = $data->manual_stop;


        // create the task
        if(
            !empty($task->task_name) &&
            !empty($task->task_content) &&
            !empty($task->master_username) &&
            //!empty($task->username) &&
            //!empty($task->public_ip) &&
            //!empty($task->hostname) &&
            //!empty($task->mac_addr) &&
            $task->create()
        ){
        
            // set response code
            http_response_code(200);
        
            echo json_encode(array(
                "message" => "Task was created.",
                "id" => $task->id
            ));
        }
        
        // message if unable to create task
        else{

            // set response code
            http_response_code(400);
        
            // display message: unable to create task
            echo json_encode(array("message" => "Unable to create task."));
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