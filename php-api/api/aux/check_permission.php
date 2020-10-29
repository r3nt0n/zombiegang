<?php

function check_permission($requested_by, $to_update=False) {
    // files needed to connect to database
    include_once 'config/database.php';
    include_once 'objects/master.php';
    
    // get database connection
    $database = new Database();
    $db = $database->getConnection();
    
    //set decoded jwt username as master requesting and check if exists
    $user_requesting = new Master($db);
    $user_to_update = new Master($db);
    $user_requesting->username = $requested_by;
    $user_to_update->username = $to_update;

    // check if request is making by a master
    $requested_by_master = $user_requesting->usernameExists();
    // check if user to update is a master
    $update_master_user = $user_to_update->usernameExists();
    
    if (!$requested_by_master) {
        throw new Exception('Not requested by master.');
    }
    // check if a master is trying to update another master
    elseif ($to_update && $update_master_user && 
            $user_requesting->username !== $user_to_update->username)  {
                throw new Exception('Masters can\'t update other masters.');
    }
}
?>