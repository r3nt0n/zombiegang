<?php
// auxilar functions
include_once 'util/prepare_queries.php';

// 'mission' object
class Mission{
 
        // database connection and table name
        private $conn;
        private $table_name = "Missions";
    
        // object properties
        public $id;
        public $created_at;
        public $updated_at;

        public $task_id;
        public $zombie_username;
        public $read_confirm;
        public $running;
        public $result;
        public $exec_at;
        public $manual_stop;
    
        // constructor
        public function __construct($db){
            $this->conn = $db;
        }

    // check if given zombie_username exist in the database
    function idExists(){
    
        // query to check if zombie_username exists
        $query = "SELECT id, created_at, updated_at, task_id, zombie_username, read_confirm, running, result, exec_at, manual_stop
                FROM " . $this->table_name . "
                WHERE id = ?
                LIMIT 0,1";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);
    
        // sanitize
        $this->id=htmlspecialchars(strip_tags($this->id));
        
        // bind given id value
        $stmt->bindParam(1, $this->id);
    
        // execute the query
        $stmt->execute();
    
        // get number of rows
        $num = $stmt->rowCount();
    
        // if zombie_username exists, assign values to object properties for easy access and use for php sessions
        if($num>0){
    
            // get record details / values
            $row = $stmt->fetch(PDO::FETCH_ASSOC);

            // assign values to object properties
            $this->id = $row["id"];
            $this->created_at = $row["created_at"];
            $this->updated_at = $row["updated_at"];

            if (empty($this->task_id)) {
                $this->task_id = $row["task_id"];
            }
            if (empty($this->zombie_username)) {
                $this->zombie_username = $row["zombie_username"];
            }
            if (empty($this->read_confirm)) {
                $this->read_confirm = $row["read_confirm"];
            }
            if (empty($this->running)) {
                $this->running = $row["running"];
            }
            if (empty($this->result)) {
                $this->result = $row["result"];
            }
            if (empty($this->exec_at)) {
                $this->exec_at = $row["exec_at"];
            }
            if (empty($this->manual_stop)) {
                $this->manual_stop = $row["manual_stop"];
            }
    
            // return true because zombie_username exists in the database
            return true;
        }
    
        // return false if zombie_username does not exist in the database
        return false;
    }

    // create new record
    function create(){
        // craft the query
        $columns_to_set = "";

        if (!empty($this->task_id)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "task_id = :task_id";
        }
        if (!empty($this->zombie_username)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "zombie_username = :zombie_username";
        }
        if (!empty($this->read_confirm)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "read_confirm = :read_confirm";
        }
        if (!empty($this->running)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "running = :running";
        }
        if (!empty($this->result)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "result = :result";
        }
        if (!empty($this->exec_at)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "exec_at = :exec_at";
        }
        if (!empty($this->manual_stop)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "manual_stop = :manual_stop";
        }

        if (!$columns_to_set) {
            return True;
        }

        // insert query
        $query = "INSERT INTO " . $this->table_name . "
                SET
                    {$columns_to_set}";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);

        if(!empty($this->task_id)){
            $this->task_id=htmlspecialchars(strip_tags($this->task_id));
            $stmt->bindParam(':task_id', $this->task_id);
        }
        if(!empty($this->zombie_username)){
            $this->zombie_username=htmlspecialchars(strip_tags($this->zombie_username));
            $stmt->bindParam(':zombie_username', $this->zombie_username);
        }
        if(!empty($this->read_confirm)){
            $this->read_confirm=htmlspecialchars(strip_tags($this->read_confirm));
            $stmt->bindParam(':read_confirm', $this->read_confirm);
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
        if(!empty($this->manual_stop)){
            $this->manual_stop=htmlspecialchars(strip_tags($this->manual_stop));
            $stmt->bindParam(':manual_stop', $this->manual_stop);
        }
    
        // execute the query, also check if query was successful
        if($stmt->execute()){
            $this->id = $this->conn->lastInsertId();
            return true;
        }
        return false;
    }

    // update a record
    public function update(){

        // craft the query
        $columns_to_set = "";

        if (!empty($this->task_id)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "task_id = :task_id";
        }
        if (!empty($this->zombie_username)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "zombie_username = :zombie_username";
        }
        if (!empty($this->read_confirm)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "read_confirm = :read_confirm";
        }
        if (!empty($this->running)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "running = :running";
        }
        if (!empty($this->result)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "result = :result";
        }
        if (!empty($this->exec_at)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "exec_at = :exec_at";
        }
        if (!empty($this->manual_stop)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set . "manual_stop = :manual_stop";
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


        if(!empty($this->task_id)){
            $this->task_id=htmlspecialchars(strip_tags($this->task_id));
            $stmt->bindParam(':task_id', $this->task_id);
        }
        if(!empty($this->zombie_username)){
            $this->zombie_username=htmlspecialchars(strip_tags($this->zombie_username));
            $stmt->bindParam(':zombie_username', $this->zombie_username);
        }
        if(!empty($this->read_confirm)){
            $this->read_confirm=htmlspecialchars(strip_tags($this->read_confirm));
            $stmt->bindParam(':read_confirm', $this->read_confirm);
        }
        if(!empty($this->running)){
            $this->running=htmlspecialchars(strip_tags($this->running));
            $stmt->bindParam(':running', $this->running);
        }
        if(!empty($this->result)){
            $this->result=htmlspecialchars(strip_tags($this->result));
            $stmt->bindParam(':result', $this->result);
        }
        if(!empty($this->exec_at && $this->exec_at)){
            $this->exec_at=htmlspecialchars(strip_tags($this->exec_at));
            $stmt->bindParam(':exec_at', $this->exec_at);
        }
        if(!empty($this->manual_stop)){
            $this->manual_stop=htmlspecialchars(strip_tags($this->manual_stop));
            $stmt->bindParam(':manual_stop', $this->manual_stop);
        }
    
        // unique ID of record to be edited
        $stmt->bindParam(':id', $this->id);
        
        if($this->idExists()) {
            // execute the query
            if($stmt->execute()){
                return true;
            }
            //print_r($stmt->errorInfo());
            // print_r($query);
            
            return false;
        }
    }    

    public function delete(){
        if($this->idExists()) {
            // query
            $query = "DELETE FROM " . $this->table_name . "
            WHERE id = ?";
        
            // prepare the query
            $stmt = $this->conn->prepare($query);
        
            // sanitize
            //$this->zombie_username=htmlspecialchars(strip_tags($this->zombie_username));
        
            // bind the values from the form
            //$stmt->bindParam(':zombie_username', $this->zombie_username);   
            // unique ID of record to be deleted
            $stmt->bindParam(1, $this->id);
        
            // execute the query
            if($stmt->execute()){
                return true;
            }
        
            return false;
        }
    }

    function read($by_id=False, $by_task_id=False, $by_read_confirm=False, $by_zombie_username=False, $by_created_at_bef=False, $by_created_at_aft=False, 
                  $zombie_view=False, $order_by='id'){


        // craft WHERE clause
        $filter = " WHERE ";

        // filter by zombie_username
        if ($by_zombie_username && $by_zombie_username !== '') {
            $filter = $filter . " zombie_username = :zombie_username";
        }
        if ($by_id) {
            // add AND if needed
            // if ($by_username or $by_submit_at_aft) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "id = :id";
        }
        if ($by_task_id) {
            // add AND if needed
            // if ($by_username or $by_submit_at_aft) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "task_id = :task_id";
        }
        if ($by_read_confirm) {
            // add AND if needed
            // if ($by_username or $by_submit_at_aft) {$filter = $filter . " AND ";}
            if (strlen($filter) > 7) {$filter = $filter . " AND ";}
            $filter = $filter . "read_confirm = :read_confirm";
        }
        
        // // set empty if filter or order_by not provided
        if (strlen($filter) == 7) { $filter = ""; }
        
        $order_by = ($order_by) ? " ORDER BY " . $order_by : 'id' ;

        $params = 'id, created_at, updated_at, task_id, zombie_username, read_confirm, running, result, exec_at, manual_stop';
        if ($zombie_view) {$params = 'id, task_id, read_confirm, running, result, exec_at, manual_stop';}

        // query
        $query = "SELECT {$params}
                FROM " . $this->table_name . "
                {$filter}
                {$order_by} DESC";
    

        // prepare the query
        $stmt = $this->conn->prepare( $query );

        //print_r($query);

        // sanitize, and bind filters
        if($by_id){
            $id=htmlspecialchars(strip_tags($by_id));
            $stmt->bindParam(':id', $id);
        }
        if($by_zombie_username){
            $zombie_username=htmlspecialchars(strip_tags($by_zombie_username));
            $stmt->bindParam(':zombie_username', $zombie_username);
        }
        if($by_task_id){
            $task_id=htmlspecialchars(strip_tags($by_task_id));
            $stmt->bindParam(':task_id', $task_id);
        }
        if($by_read_confirm){
            $read_confirm=htmlspecialchars(strip_tags($by_read_confirm));
            $stmt->bindParam(':read_confirm', $read_confirm);
        }
    
        // execute the query
        $stmt->execute();
    
        // get number of rows
        $num = $stmt->rowCount();
    
        // if zombie_username exists, assign values to object properties for easy access and use for php sessions
        if($num>0){
    
            // get record details / values
            $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
            // return true because zombie_username exists in the database
            return $rows;
        }
        //print_r($query);
        //print_r($stmt->errorInfo());
        // return false if any log exists
        return false;
    }
}

?>
