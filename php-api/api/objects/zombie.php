<?php
// auxilar functions
include_once 'util/prepare_queries.php';

// 'user' object
class Zombie{
 
    // database connection and table name
    private $conn;
    private $table_name = "Zombies";

    // object properties
    public $id;
    public $created_at;
    public $updated_at;
    public $last_seen;

    public $username;
    public $os;
    public $current_public_ip;
    public $current_country;
    public $current_hostname;
    public $refresh_secs;

    // constructor
    public function __construct($db){
        $this->conn = $db;
    }


    // check if given username exist in the database
    function usernameExists(){

        // query to check if username exists
        $query = "SELECT id, username, created_at, updated_at, last_seen, os, current_public_ip, current_country, current_hostname, refresh_secs
                FROM " . $this->table_name . "
                WHERE username = ?
                LIMIT 0,1";
    
        // prepare the query
        $stmt = $this->conn->prepare( $query );
    
        // sanitize
        $this->username=htmlspecialchars(strip_tags($this->username));
    
        // bind given username value
        $stmt->bindParam(1, $this->username);
    
        // execute the query
        $stmt->execute();
    
        // get number of rows
        $num = $stmt->rowCount();
    
        // if username exists, assign values to object properties for easy access and use for php sessions
        if($num>0){
    
            // get record details / values
            $row = $stmt->fetch(PDO::FETCH_ASSOC);
    
            // assign values to object properties
            $this->id = $row['id'];
            $this->created_at = $row['created_at'];
            $this->updated_at = $row['updated_at'];
            $this->last_seen = $row['last_seen'];
            $this->username = $row['username'];
            $this->os = $row['os'];
            $this->current_public_ip = $row['current_public_ip'];
            $this->current_country = $row['current_country'];
            $this->current_hostname = $row['current_hostname'];
            $this->refresh_secs = $row['refresh_secs'];
    
            // return true because username exists in the database
            return true;
        }
    
        // return false if username does not exist in the database
        return false;
    }

    // create new record
    function create(){
        if(!$this->usernameExists()) {
            // insert query
            $query = "INSERT INTO " . $this->table_name . "
                    SET
                        username = :username,
                        os = :os,
                        current_public_ip = :current_public_ip,
                        current_country = :current_country,
                        current_hostname = :current_hostname";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            $this->username=htmlspecialchars(strip_tags($this->username));
            $this->os=htmlspecialchars(strip_tags($this->os));
            $this->current_public_ip=htmlspecialchars(strip_tags($this->current_public_ip));
            $this->current_country=htmlspecialchars(strip_tags($this->current_country));
            $this->current_hostname=htmlspecialchars(strip_tags($this->current_hostname));
        
            // bind the values
            $stmt->bindParam(':username', $this->username);
            $stmt->bindParam(':os', $this->os);
            $stmt->bindParam(':current_public_ip', $this->current_public_ip);
            $stmt->bindParam(':current_country', $this->current_country);
            $stmt->bindParam(':current_hostname', $this->current_hostname);
        
            // execute the query, also check if query was successful
            if(!$this->usernameExists() && $stmt->execute()){
                return true;
            }
        
            return false;
        }
    }

    // update record
    public function update(){

        if($this->usernameExists()) {

            $columns_to_update = "";
            $columns_to_update = !empty($this->os) ? "os = :os" : "";
            if (!empty($this->current_public_ip)) {
                if (!empty($columns_to_update)) { $columns_to_update += ', ';}
                $columns_to_update += "current_public_ip = :current_public_ip";
            }
            if (!empty($this->current_country)) {
                if (!empty($columns_to_update)) { $columns_to_update += ', ';}
                $columns_to_update += "current_country = :current_country";
            }
            if (!empty($this->current_hostname)) {
                if (!empty($columns_to_update)) { $columns_to_update += ', ';}
                $columns_to_update += "current_hostname = :current_hostname";
            }
            if (!empty($this->refresh_secs)) {
                if (!empty($columns_to_update)) { $columns_to_update += ', ';}
                $columns_to_update += "refresh_secs = :refresh_secs";
            }
            if (!$columns_to_update) {
                return True;
            }
 
            // if no posted password, do not update the password
            $query = "UPDATE " . $this->table_name . "
                    SET
                        {$columns_to_update}
                    WHERE id = :id";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->username=htmlspecialchars(strip_tags($this->username));
            $this->os=htmlspecialchars(strip_tags($this->os));
            $this->current_public_ip=htmlspecialchars(strip_tags($this->current_public_ip));
            $this->current_country=htmlspecialchars(strip_tags($this->current_country));
            $this->current_hostname=htmlspecialchars(strip_tags($this->current_hostname));
            $this->refresh_secs=htmlspecialchars(strip_tags($this->refresh_secs));
        
            // bind the values from the form
            //$stmt->bindParam(':username', $this->username);
            if(!empty($this->os)){
                $stmt->bindParam(':os', $this->os);
            }
            if(!empty($this->current_public_ip)){
                $stmt->bindParam(':current_public_ip', $this->current_public_ip);
            }
            if(!empty($this->current_country)){
                $stmt->bindParam(':current_country', $this->current_country);
            }
            if(!empty($this->current_hostname)){
                $stmt->bindParam(':current_hostname', $this->current_hostname);
            }
            if(!empty($this->refresh_secs)){
                $stmt->bindParam(':refresh_secs', $this->refresh_secs);
            }
            // unique ID of record to be edited
            $stmt->bindParam(':id', $this->id);
        
            // execute the query
            if($stmt->execute()){
                return true;
            }
        
            return false;
        }
    }

    public function delete(){
        if($this->usernameExists()) {
            // query
            $query = "DELETE FROM " . $this->table_name . "
            WHERE id = ?";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->username=htmlspecialchars(strip_tags($this->username));
        
            // bind the values from the form
            //$stmt->bindParam(':username', $this->username);
            // unique ID of record to be deleted
            $stmt->bindParam(1, $this->id);
        
            // execute the query
            if($stmt->execute()){
                return true;
            }
        
            return false;
        }
    }

    function read($filter_by_username=False, $filter_by_datetime_bef=False,$filter_by_datetime_aft=False, 
                  $filter_by_os=False, $order_by='id'){

        // craft WHERE clause
        $filter = " WHERE ";

        // filter by username
        if ($filter_by_username && $filter_by_username !== '') {
            $filter = $filter . " username = :username";
            $enable_AND = True;
        }
        
        // filter by datetime
        if ($filter_by_datetime_aft) {
            //if ($filter_by_username) {$filter = $filter . " AND ";}
            if ($enable_AND) {$filter = $filter . " AND ";}
            else {$enable_AND = True;}
            $filter = $filter . "created_at >= :datetime_aft";
            }
        if ($filter_by_datetime_bef) {
            //if ($filter_by_username or $filter_by_datetime_aft) {$filter = $filter . " AND ";}
            if ($enable_AND) {$filter = $filter . " AND ";}
            else {$enable_AND = True;}
            $filter = $filter . "created_at <= :datetime_bef";
        }

        // filter by os
        if ($filter_by_os) {
            if ($enable_AND) {$filter = $filter . " AND ";}
            else {$enable_AND = True;}
            $filter = $filter . "os = :os";
        }

        // set empty if filter or order_by not provided
        if (!$filter_by_username && !$filter_by_datetime_aft && !$filter_by_datetime_bef && !$filter_by_os) { $filter = ""; }
        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        // query
        $query = "SELECT id, username, created_at, updated_at, last_seen, os, current_public_ip, current_country, current_hostname, refresh_secs
                FROM " . $this->table_name . "
                {$filter}
                {$order_by} DESC";
    

        // prepare the query
        $stmt = $this->conn->prepare( $query );

        // sanitize, and bind filters
        if($filter_by_username){
            $username=htmlspecialchars(strip_tags($filter_by_username));
            $stmt->bindParam(':username', $username);
        }
        if($filter_by_os){
            $os=htmlspecialchars(strip_tags($filter_by_os));
            $stmt->bindParam(':os', $os);
        }
        if($filter_by_datetime_aft){
            $datetime_aft=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_datetime_aft)) . ":00"));
            //$datetime_aft=(date('Y-m-d H:i:s', strtotime($filter_by_datetime_aft)));
            $stmt->bindParam(':datetime_aft', $datetime_aft);
        }
        if($filter_by_datetime_bef){
            $datetime_bef=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_datetime_bef)) . ":00"));
            $stmt->bindParam(':datetime_bef', $datetime_bef);
        }

        //print_r($query);
    
        // execute the query
        $stmt->execute();
    
        // get number of rows
        $num = $stmt->rowCount();
    
        // if username exists, assign values to object properties for easy access and use for php sessions
        if($num>0){
    
            // get record details / values
            $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
            // return true because username exists in the database
            return $rows;
        }
        //print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }

}

?>
