<?php

// 'task' object
class Task{
 
        // database connection and table name
        private $conn;
        private $table_name = "Tasks";
    
        // object properties
        public $task_type;
        public $task_content;
        public $master_username;
        public $submit_at;
        public $to_exec_at;
        public $to_stop_at;
        public $zombie_username;
        public $readed;
        public $running;
        public $result;
        public $exec_at;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

        // check if given task exist in the database
        function IdExists(){
    
            // query to check if task exists
            $query = "SELECT id, task_type, task_content, master_username, submit_at, to_exec_at, to_stop_at, zombie_username, readed, result, exec_at
                    FROM " . $this->table_name . "
                    WHERE id = ?
                    LIMIT 0,1";
        
            // prepare the query
            $stmt = $this->conn->prepare( $query );
        
            // sanitize
            $this->id=htmlspecialchars(strip_tags($this->id));
        
            // bind given id value
            $stmt->bindParam(1, $this->id);
        
            // execute the query
            $stmt->execute();
        
            // get number of rows
            $num = $stmt->rowCount();
        
            // if task exists, assign values to object properties for easy access and use for php sessions
            if($num>0){
        
                // get record details / values
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
                // assign values to object properties
                $this->id = $row['id'];
                if (empty($this->task_type)) {
                    $this->task_type = $row['task_type'];
                }
                if (empty($this->task_content)) {
                    $this->task_content = $row['task_content'];
                }
                if (empty($this->master_username)) {
                    $this->master_username = $row['master_username'];
                }
                if (empty($this->submit_at)) {
                    $this->submit_at = $row['submit_at'];
                }
                if (empty($this->to_exec_at)) {
                    $this->to_exec_at = $row['to_exec_at'];
                }
                if (empty($this->to_stop_at)) {
                    $this->to_stop_at = $row['to_stop_at'];
                }
                if (empty($this->zombie_username)) {
                    $this->zombie_username = $row['zombie_username'];
                }
                if (empty($this->running)) {
                    $this->running = $row['running'];
                }
                if (empty($this->result)) {
                    $this->result = $row['result'];
                }
                if (empty($this->exec_at)) {
                    $this->exec_at = $row['exec_at'];
                }
        
                // return true because task exists in the database
                return true;
            }
        
            // return false if task does not exist in the database
            return false;
        }

    // create new access-log record
    function create(){

        $columns_to_set = "";
        $columns_to_set = (!empty($this->task_type)) ? "task_type = :task_type" : "";
        if (!empty($this->task_content)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}
            $columns_to_set = $columns_to_set .  "task_content = :task_content";
        }
        if (!empty($this->master_username)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "master_username = :master_username";
        }
        if (!empty($this->to_exec_at)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "to_exec_at = :to_exec_at";
        }
        if (!empty($this->to_stop_at)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "to_stop_at = :to_stop_at";
        }
        if (!empty($this->zombie_username)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "zombie_username = :zombie_username";
        }
        if (!empty($this->readed)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "readed = :readed";
        }
        if (!empty($this->running)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "running = :running";
        }
        if (!empty($this->result)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "result = :result";
        }
        if (!empty($this->exec_at)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            $columns_to_set = $columns_to_set .  "exec_at = :exec_at";
        }

    
        // insert query
        $query = "INSERT INTO " . $this->table_name . "
                SET
                    {$columns_to_set}";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);
        //print_r($query);
        //print_r($this->task_content);

        // sanitize and bind
        if(!empty($this->task_type)){
            $this->task_type=htmlspecialchars(strip_tags($this->task_type));
            $stmt->bindParam(':task_type', $this->task_type);
        }
        if(!empty($this->task_content)){
            $this->task_content=htmlspecialchars(strip_tags($this->task_content));
            $stmt->bindParam(':task_content', $this->task_content);
        }
        if(!empty($this->master_username)){
            $this->master_username=htmlspecialchars(strip_tags($this->master_username));
            $stmt->bindParam(':master_username', $this->master_username);
        }
        // if(!empty($this->submit_at)){
        //     $stmt->bindParam(':submit_at', $this->submit_at);
        // }
        if(!empty($this->to_exec_at)){
            $this->to_exec_at=htmlspecialchars(strip_tags($this->to_exec_at));
            $stmt->bindParam(':to_exec_at', $this->to_exec_at);
        }
        if(!empty($this->to_stop_at)){
            $this->to_stop_at=htmlspecialchars(strip_tags($this->to_stop_at));
            $stmt->bindParam(':to_stop_at', $this->to_stop_at);
        }
        if(!empty($this->zombie_username)){
            $this->zombie_username=htmlspecialchars(strip_tags($this->zombie_username));
            $stmt->bindParam(':zombie_username', $this->zombie_username);
        }
        if(!empty($this->readed)){
            $this->readed=htmlspecialchars(strip_tags($this->readed));
            $stmt->bindParam(':readed', $this->readed);
        }
        if(!empty($this->running)){
            $this->running=htmlspecialchars(strip_tags($this->running));
            $stmt->bindParam(':running', $this->running);
        }
        if(!empty($this->result)){
            $this->result=htmlspecialchars(strip_tags($this->result));
            $stmt->bindParam(':result', $this->result);
        }
        if(!empty($this->exec_at)){
            $this->exec_at=htmlspecialchars(strip_tags($this->exec_at));
            $stmt->bindParam(':exec_at', $this->exec_at);
        }
    
        // execute the query, also check if query was successful
        if($stmt->execute()){
            return true;
        }
        //print_r($stmt->errorInfo());  // only for debug purpose
        return false;
    }


    // update a user record
    public function update(){
        if($this->IdExists()) {

            // craft the query
            $columns_to_set = "";
            $columns_to_set = (!empty($this->task_type)) ? "task_type = :task_type" : "";
            if (!empty($this->task_content)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "task_content = :task_content";
            }
            if (!empty($this->master_username)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "master_username = :master_username";
            }
            // if (!empty($this->submit_at)) {
            //     if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
            //     $columns_to_set = $columns_to_set .  "submit_at = :submit_at";
            // }
            if (!empty($this->to_exec_at)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "to_exec_at = :to_exec_at";
            }
            if (!empty($this->to_stop_at)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "to_stop_at = :to_stop_at";
            }
            if (!empty($this->zombie_username)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "zombie_username = :zombie_username";
            }
            if (!empty($this->readed)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "readed = :readed";
            }
            if (!empty($this->running)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "running = :running";
            }
            if (!empty($this->result)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "result = :result";
            }
            if (!empty($this->exec_at)) {
                if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set .  ', ';}
                $columns_to_set = $columns_to_set .  "exec_at = :exec_at";
            }
            if (!$columns_to_set) {
                return True;
            }
 
            // query
            $query = "UPDATE " . $this->table_name . "
                    SET
                        {$columns_to_set}
                    WHERE id = :id";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize and bind
            if(!empty($this->task_type)){
                $this->task_type=htmlspecialchars(strip_tags($this->task_type));
                $stmt->bindParam(':task_type', $this->task_type);
            }
            if(!empty($this->task_content)){
                $this->task_content=htmlspecialchars(strip_tags($this->task_content));
                $stmt->bindParam(':task_content', $this->task_content);
            }
            if(!empty($this->master_username)){
                $this->master_username=htmlspecialchars(strip_tags($this->master_username));
                $stmt->bindParam(':master_username', $this->master_username);
            }
            // if(!empty($this->submit_at)){
            //     $stmt->bindParam(':submit_at', $this->submit_at);
            // }
            if(!empty($this->to_exec_at)){
                $this->to_exec_at=htmlspecialchars(strip_tags($this->to_exec_at));
                $stmt->bindParam(':to_exec_at', $this->to_exec_at);
            }
            if(!empty($this->to_stop_at)){
                $this->to_stop_at=htmlspecialchars(strip_tags($this->to_stop_at));
                $stmt->bindParam(':to_stop_at', $this->to_stop_at);
            }
            if(!empty($this->zombie_username)){
                $this->zombie_username=htmlspecialchars(strip_tags($this->zombie_username));
                $stmt->bindParam(':zombie_username', $this->zombie_username);
            }
            if(!empty($this->readed)){
                $this->readed=htmlspecialchars(strip_tags($this->readed));
                $stmt->bindParam(':readed', $this->readed);
            }
            if(!empty($this->running)){
                $this->running=htmlspecialchars(strip_tags($this->running));
                $stmt->bindParam(':running', $this->running);
            }
            if(!empty($this->result)){
                $this->result=htmlspecialchars(strip_tags($this->result));
                $stmt->bindParam(':result', $this->result);
            }
            if(!empty($this->exec_at)){
                $this->exec_at=htmlspecialchars(strip_tags($this->exec_at));
                $stmt->bindParam(':exec_at', $this->exec_at);
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

        if($this->IdExists()) {
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


    function read($filter_by_username=False, $filter_by_submit_at_bef=False,$filter_by_submit_at_aft=False, $order_by='id', $zombie_view=False){

        if ($filter_by_submit_at_aft == " ") { $filter_by_submit_at_aft = "";}
        if ($filter_by_submit_at_bef == " ") { $filter_by_submit_at_bef = "";}

        // craft WHERE clause
        $filter = " WHERE ";

        // filter by task
        if ($filter_by_username && $filter_by_username !== '') {
            $filter = $filter . " zombie_username = :zombie_username";
        }
        
        // filter by datetime
        if ($filter_by_submit_at_aft) {
            // add AND if needed
            // if ($filter_by_username) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "date_time >= :submit_at_aft";
            }
        if ($filter_by_submit_at_bef) {
            // add AND if needed
            // if ($filter_by_username or $filter_by_submit_at_aft) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "date_time <= :submit_at_bef";
        }

        // set empty if filter or order_by not provided
        // if (!$filter_by_username && !$filter_by_submit_at_aft && !$filter_by_submit_at_bef) { $filter = ""; }
        if (strlen($filter) == 7) { $filter = ""; }
        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        // set view depending on user type requesting
        $params = 'id, task_type, task_content, master_username, submit_at, to_exec_at, to_stop_at, zombie_username, readed, result, exec_at';
        if ($zombie_view) {$params = 'id, task_type, task_content, to_exec_at, to_stop_at, readed';}

        // query
        $query = "SELECT {$params}
                FROM " . $this->table_name . "
                {$filter}
                {$order_by} DESC";

        //print_r($query);
    
        // prepare the query
        $stmt = $this->conn->prepare( $query );

        // sanitize, and bind filters
        if($filter_by_username){
            $username=htmlspecialchars(strip_tags($filter_by_username));
            $stmt->bindParam(':zombie_username', $username);
        }
        if($filter_by_submit_at_aft){
            $submit_at_aft=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_submit_at_aft)) . ":00"));
            //$submit_at_aft=(date('Y-m-d H:i:s', strtotime($filter_by_submit_at_aft)));
            $stmt->bindParam(':submit_at_aft', $submit_at_aft);
        }
        if($filter_by_submit_at_bef){
            $submit_at_bef=htmlspecialchars(strip_tags(date('Y-m-d H:i:s', strtotime($filter_by_submit_at_bef)) . ":00"));
            $stmt->bindParam(':submit_at_bef', $submit_at_bef);
        }
    
        // execute the query
        $stmt->execute();
    
        // get number of rows
        $num = $stmt->rowCount();
    
        // if task exists, assign values to object properties for easy access and use for php sessions
        if($num>0){
    
            // get record details / values
            $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
            // return true because task exists in the database
            return $rows;
        }
        //print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }







}

?>
