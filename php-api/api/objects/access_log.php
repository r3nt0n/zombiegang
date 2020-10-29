<?php

// 'user' object
class AccessLog{
 
        // database connection and table name
        private $conn;
        private $table_name = "AccessLogs";
    
        // object properties
        public $successful;
        public $username;
        public $public_ip;
        public $hostname;
        public $mac_addr;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

    // create new access-log record
    function create(){
    
        // insert query
        $query = "INSERT INTO " . $this->table_name . "
                SET
                    successful = :successful,
                    username = :username,
                    public_ip = :public_ip,
                    hostname = :hostname,
                    mac_addr = :mac_addr";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);

        // sanitize
        $this->username=htmlspecialchars(strip_tags($this->username));
        $this->public_ip=htmlspecialchars(strip_tags($this->public_ip));
        $this->hostname=htmlspecialchars(strip_tags($this->hostname));
        $this->mac_addr=htmlspecialchars(strip_tags($this->mac_addr));
        
        //echo $this->public_ip;

        // bind the values
        $stmt->bindParam(':successful', $this->successful);
        $stmt->bindParam(':username', $this->username);
        $stmt->bindParam(':public_ip', $this->public_ip);
        $stmt->bindParam(':hostname', $this->hostname);
        $stmt->bindParam(':mac_addr', $this->mac_addr);
    
        // execute the query, also check if query was successful
        if($stmt->execute()){
            return true;
        }
        //print_r($stmt->errorInfo());  // only for debug purpose
        return false;
    }


    function read($filter_by_username=False, $filter_by_datetime_bef=False,$filter_by_datetime_aft=False , $order_by='id'){

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
            if ($filter_by_username) {$filter = $filter . " AND ";}
            $filter = $filter . "date_time >= :datetime_aft";
            }
        if ($filter_by_datetime_bef) {
            // add AND if needed
            if ($filter_by_username or $filter_by_datetime_aft) {$filter = $filter . " AND ";}
            // elseif ($filter_by_datetime_aft) {$filter = $filter . " OR ";}
            $filter = $filter . "date_time <= :datetime_bef";
        }

        // set empty if filter or order_by not provided
        if (!$filter_by_username && !$filter_by_datetime_aft && !$filter_by_datetime_bef) { $filter = ""; }
        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        // query
        $query = "SELECT id, date_time, successful, username, public_ip, hostname, mac_addr
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
        //print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }







}

?>
