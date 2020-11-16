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
include_once 'objects/task.php';

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

        // get database connection
        $database = new Database();
        $db = $database->getConnection();

        // Check who request and permission
        $requested_by = $decoded->data->username;
        
        $task = new Task($db);
        $task->id = $data->task_id;
        $task_author = ($task->idExists()) ? $task->master_username : False;
        if (!$task_author) {
            // set response code
            http_response_code(401);
        
            // show error message
            echo json_encode(array(
                "message" => "task id not found."
            ));
            return False;
        }
        else{
            // this function raise exceptions in case of error (not requested by a mission, or requesting changes on another mission)
            check_master_permissions($requested_by, $task_author);
        }
        
        // instantiate user object
        $mission = new Mission($db);
        // set mission property values
        $mission->task_id = $data->task_id;
        $mission->zombie_username = $data->zombie_username;
        $mission->read_confirm = $data->read_confirm;
        $mission->running = $data->running;
        $mission->result = $data->result;
        $mission->exec_at = $data->exec_at;

        // create the user
        if(
            // !empty($mission->master_username) &&
            $mission->create()
        ){
        
            // set response code
            http_response_code(200);
        
            // display message: user was created
            echo json_encode(array(
                "message" => "Mission was created.",
                "id" => $mission->id
            ));
        }
        
        // message if unable to create mission
        else{

            // set response code
            http_response_code(400);
        
            // display message: unable to create mission
            echo json_encode(array("message" => "Unable to create mission."));
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