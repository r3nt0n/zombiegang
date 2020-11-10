<?php

function is_master($db, $username) {
    include_once 'objects/master.php';
    $user_to_check = new Master($db);
    $user_to_check->username = $username;
    return $user_to_check->usernameExists();
}

function is_zombie($db, $username) {
    include_once 'objects/zombie.php';
    $user_to_check = new Zombie($db);
    $user_to_check->username = $username;
    return $user_to_check->usernameExists();
}

function check_master_permissions($requested_by, $to_update=False) {
    // files needed to connect to database
    include_once 'config/database.php';
    
    // get database connection
    $database = new Database();
    $db = $database->getConnection();

    // check if request is making by a master
    $requested_by_master = is_master($db, $requested_by);
    // check if user to update is a master
    $update_master_user = is_master($db, $to_update);
    
    if (!$requested_by_master) {
        throw new Exception('Not requested by master.');
    }
    // check if a master is trying to update another master
    elseif ($to_update && $update_master_user && 
            $user_requesting->username !== $user_to_update->username)  {
                throw new Exception('Masters can\'t update/delete other masters or objects created by other masters.');
    }
}

?>