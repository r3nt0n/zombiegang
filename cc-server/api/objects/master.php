<?php
// auxilar functions
include_once 'util/prepare_queries.php';

// 'master' object
class Master{
 
        // database connection and table name
        private $conn;
        private $table_name = "Masters";
    
        // object properties
        public $id;
        public $created_at;
        public $updated_at;
        
        public $username;
        public $public_key;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

    // check if given username exist in the database
    function usernameExists(){
    
        // query to check if username exists
        $query = "SELECT id, created_at, updated_at, username, public_key
                FROM " . $this->table_name . "
                WHERE username = ?
                LIMIT 0,1";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);
    
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
            if (empty($this->username)) {
                $this->username = $row['username'];
            }
            if (empty($this->public_key)) {
                $this->public_key = $row['public_key'];
            }
    
            // return true because username exists in the database
            return true;
        }
    
        // return false if username does not exist in the database
        return false;
    }

    // create new user record
    function create(){
        if(!$this->usernameExists()) {
            // insert query
            $query = "INSERT INTO " . $this->table_name . "
                    SET
                        username = :username,
                        public_key = :public_key";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            $this->username=htmlspecialchars(strip_tags($this->username));
            $this->public_key=htmlspecialchars(strip_tags($this->public_key));
        
            // bind the values
            $stmt->bindParam(':username', $this->username);
            $stmt->bindParam(':public_key', $this->public_key);
        
            // execute the query, also check if query was successful
            if(!$this->usernameExists() && $stmt->execute()){
                return true;
            }
        
            return false;
        }
    }

    
 
    // update a user record
    public function update(){
        if($this->usernameExists()) {

            $public_key_set = !empty($this->public_key) ? "SET public_key = :public_key" : "";

            if (!$public_key_set) {
                return True;
            }

            // if no posted password, do not update the password
            $query = "UPDATE " . $this->table_name . "
                    SET
                        {$public_key_set}
                    WHERE id = :id";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->username=htmlspecialchars(strip_tags($this->username));
            $this->public_key=htmlspecialchars(strip_tags($this->public_key));
        
            // bind the values from the form
            //$stmt->bindParam(':username', $this->username);
            $stmt->bindParam(':public_key', $this->public_key);
        
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

    function read($filter_by_username=False, $order_by='id'){

        // craft WHERE clause
        $filter = " WHERE ";

        // filter by username
        if ($filter_by_username && $filter_by_username !== '') {
            $filter = $filter . " username = :username";
        }
        
        // // filter by datetime
        // if ($filter_by_datetime_aft) {
        //     // add AND if needed
        //     if ($filter_by_username) {$filter = $filter . " AND ";}
        //     $filter = $filter . "created_at >= :datetime_aft";
        //     }
        // if ($filter_by_datetime_bef) {
        //     // add AND if needed
        //     if ($filter_by_username or $filter_by_datetime_aft) {$filter = $filter . " AND ";}
        //     //elseif ($filter_by_datetime_aft) {$filter = $filter . " OR ";}
        //     $filter = $filter . "created_at <= :datetime_bef";
        // }

        // // set empty if filter or order_by not provided
        if (!$filter_by_username) { $filter = ""; }
        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        // query
        $query = "SELECT id, username
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
        // if($filter_by_datetime_aft){
        //     $datetime_aft=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_datetime_aft)) . ":00"));
        //     //$datetime_aft=(date('Y-m-d H:i:s', strtotime($filter_by_datetime_aft)));
        //     $stmt->bindParam(':datetime_aft', $datetime_aft);
        // }
        // if($filter_by_datetime_bef){
        //     $datetime_bef=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_datetime_bef)) . ":00"));
        //     $stmt->bindParam(':datetime_bef', $datetime_bef);
        // }
    
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
        // print_r($query);
        // print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }
}

?>
