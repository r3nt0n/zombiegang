<?php
function create_access_log($log_data){
    // required headers (not need as long as this is a function and only can be executed from other files)
    // header("Access-Control-Allow-Origin: *");
    // header("Content-Type: application/json; charset=UTF-8");
    // header("Access-Control-Allow-Methods: POST");
    // header("Access-Control-Max-Age: 3600");
    // header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
    
    // files needed to connect to database
    include_once 'config/database.php';  // paths are relative to page who imports function
    include_once 'objects/access_log.php';

    // get database connection
    $database = new Database();
    $db = $database->getConnection();
    
    // instantiate access_log object
    $access_log = new AccessLog($db);
    
    // get posted data - NOT (this is not accessible from outside)
    //$data = json_decode(file_get_contents("php://input"));
    
    // set access_log property values
    $access_log->successful = $log_data["successful"];
    $access_log->username = $log_data["username"];
    $access_log->public_ip = $log_data["public_ip"];
    $access_log->country = $log_data["country"];
    $access_log->hostname = $log_data["hostname"];

    //echo $access_log->successful;

    // create the access_log
    if(
        //!empty($access_log->successful) &&
        //!empty($access_log->username) &&
        //!empty($access_log->public_ip) &&
        //!empty($access_log->hostname) &&
        $access_log->create()
    ){
    
        // set response code
        http_response_code(200);
    
        // display message: access_log was created
        // silent access log creation
        //echo json_encode(array("message" => "access_log was created."));
    }
    
    // message if unable to create access_log
    else{

        // set response code
        http_response_code(400);
    
        // display message: unable to create access_log
        echo json_encode(array("message" => "Unable to create access_log."));
    }

}
?>