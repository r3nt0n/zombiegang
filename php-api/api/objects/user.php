<?php
// 'user' object
class User{
 
        // database connection and table name
        private $conn;
        private $table_name = "Users";
    
        // object properties
        public $username;
        public $pswd;
        public $registered_at;
        public $public_ip;
        public $country;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

    // check if given username exist in the database
    function usernameExists(){
    
        // query to check if username exists
        $query = "SELECT id, username, pswd, registered_at, public_ip, country
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
            if (empty($this->username)) {
                $this->username = $row['username'];
            }
            if (empty($this->pswd)) {
                $this->pswd = $row['pswd'];
            }
            if (empty($this->registered_at)) {
                $this->registered_at = $row['registered_at'];
            }
            if (empty($this->public_ip)) {
                $this->public_ip = $row['public_ip'];
            }
            if (empty($this->country)) {
                $this->country = $row['country'];
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
                        pswd = :pswd,
                        public_ip = :public_ip,
                        country = :country";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            $this->username=htmlspecialchars(strip_tags($this->username));
            $this->pswd=htmlspecialchars(strip_tags($this->pswd));
            $this->public_ip=htmlspecialchars(strip_tags($this->public_ip));
            $this->country=htmlspecialchars(strip_tags($this->country));
        
            // bind the values
            $stmt->bindParam(':username', $this->username);
            $stmt->bindParam(':public_ip', $this->public_ip);
            $stmt->bindParam(':country', $this->country);
            // hash the password before saving to database
            $password_hash = password_hash($this->pswd, PASSWORD_BCRYPT);
            $stmt->bindParam(':pswd', $password_hash);
        
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
            // if password needs to be updated
            //$password_set=!empty($this->pswd) ? ", pswd = :pswd" : "";
            $password_set = !empty($this->pswd) ? "SET pswd = :pswd" : "";

            if (!$password_set) {
                return True;
            }
        
            // if no posted password, do not update the password
            $query = "UPDATE " . $this->table_name . "
                    {$password_set}
                    WHERE id = :id";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->username=htmlspecialchars(strip_tags($this->username));
            // bind the values from the form
            //$stmt->bindParam(':username', $this->username);
        
            // sanitize, hash and bind the password before saving to database
            if(!empty($this->pswd)){
                $this->pswd=htmlspecialchars(strip_tags($this->pswd));
                $password_hash = password_hash($this->pswd, PASSWORD_BCRYPT);
                $stmt->bindParam(':pswd', $password_hash);
            }
        
            // unique ID of record to be edited
            $stmt->bindParam(':id', $this->id);
        
            // execute the query
            if($stmt->execute()){
                return true;
            }
            // print_r($stmt->errorInfo());
            // print_r($query);
            
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

    function read($filter_by_username=False, $filter_by_datetime_bef=False,$filter_by_datetime_aft=False, $not_in_tables="", $order_by='id'){

        if ($filter_by_datetime_aft == " ") { $filter_by_datetime_aft = "";}
        if ($filter_by_datetime_bef == " ") { $filter_by_datetime_bef = "";}

        // craft WHERE clause
        $filter = " WHERE ";

        // filter by username
        if ($filter_by_username && $filter_by_username !== '') {
            $filter = $filter . " username = :username";
        }
        
        // filter by datetime
        if ($filter_by_datetime_aft) {
            // add AND if needed
            //if ($filter_by_username) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "date_time >= :datetime_aft";
            }
        if ($filter_by_datetime_bef) {
            // add AND if needed
            //if ($filter_by_username or $filter_by_datetime_aft) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "date_time <= :datetime_bef";
        }

        //if (count($not_in_tables) > 0) {
        if ($not_in_tables) {
            // sanitize input
            $not_in_tables = htmlspecialchars(strip_tags($not_in_tables));
            // split by commas
            if (strpos($not_in_tables, ',')) {
                $not_in_tables = explode(',', $not_in_tables);
            }
            else{
                $not_in_tables = [$not_in_tables];
            }
            // add a filter for each table
            foreach ($not_in_tables as $table) {
                // add AND if needed
                //if ($filter_by_username or $filter_by_datetime_aft or $filter_by_datetime_bef) {$filter = $filter . " AND ";}
                if (strlen($filter) > 7) {$filter = $filter . " AND ";}

                // sanitize table name input
                $table=strtolower($table);
                switch ($table) {
                    case "users":
                        $sanitized_table = "Users";
                        break;
                    case "zombies":
                        $sanitized_table = "Zombies";
                        break;
                    case "masters":
                        $sanitized_table = "Masters";
                        break;
                    case "access-logs":
                        $sanitized_table = "AccessLogs";
                        break;
                    }
                // add crafted filter
                $filter = $filter . "username NOT IN (SELECT username FROM ".$sanitized_table.")";
            }
            unset($table);  // break last loop reference
        }

        // set empty if filter or order_by not provided
        //if (!$filter_by_username && !$filter_by_datetime_aft && !$filter_by_datetime_bef && (count($not_in_tables) == 0)) { $filter = ""; }
        if (strlen($filter) == 7) { $filter = ""; }

        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        // query
        $query = "SELECT id, username, registered_at, public_ip, country
                FROM " . $this->table_name . "
                {$filter}
                {$order_by} DESC";

        //print_r($query);
    
        // prepare the query
        $stmt = $this->conn->prepare( $query );

        // sanitize, and bind filters
        if($filter_by_username){
            $username=htmlspecialchars(strip_tags($filter_by_username));
            $stmt->bindParam(':username', $username);
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
        print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }

}

?>
