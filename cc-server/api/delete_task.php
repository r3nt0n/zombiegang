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

        // instantiate user object
        $task = new Task($db);

        // Check who request and permission
        $requested_by = $decoded->data->username;

        // set task property values and check if the task author and user requesting matches
        $task->id = $data->id;
        $task_author = ($task->idExists()) ? $task->master_username : False;
        
        // this function raise exceptions in case of error (not requested by a master, or requesting changes on another master)
        check_master_permissions($requested_by, $task_author);

        // delete the task record
        if($task->delete()){
            
            // set response code
            http_response_code(200);
            
            // response in json format
            echo json_encode(
                    array(
                        "message" => "User was deleted."
                    )
                );
        }
        
        // message if unable to delete user
        else{
            // set response code
            http_response_code(401);
        
            // show error message
            echo json_encode(array("message" => "Unable to delete task."));
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