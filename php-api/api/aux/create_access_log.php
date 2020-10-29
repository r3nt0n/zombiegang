<?php
function create_access_log($log_data){
    // required headers
    header("Access-Control-Allow-Origin: http://localhost/login.php");
    header("Content-Type: application/json; charset=UTF-8");
    header("Access-Control-Allow-Methods: POST");
    header("Access-Control-Max-Age: 3600");
    header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
    
    // files needed to connect to database
    include_once 'config/database.php';  // paths are relative to page who imports function
    include_once 'objects/access_log.php';

    // Only the own server can create access logs (triggered by actions like login.php)
    if (!(isset($_SERVER['SERVER_ADDR'])) or
        $_SERVER['SERVER_ADDR'] == $_SERVER['REMOTE_ADDR']){

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
        $access_log->hostname = $log_data["hostname"];
        $access_log->mac_addr = $log_data["mac_addr"];

        //echo $access_log->successful;

        // create the access_log
        if(
            //!empty($access_log->successful) &&
            //!empty($access_log->username) &&
            //!empty($access_log->public_ip) &&
            //!empty($access_log->hostname) &&
            //!empty($access_log->mac_addr) &&
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

    else {
        // set response code
        http_response_code(403);
    
        // display message: access_log was created
        echo json_encode(array("message" => "No remote access allowed."));
        exit; //just for good measure
    }
}
?>