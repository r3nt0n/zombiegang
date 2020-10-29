<?php
// 'user' object
class User{
 
        // database connection and table name
        private $conn;
        private $table_name = "Users";
    
        // object properties
        public $username;
        public $pswd;
    
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
                    pswd = :pswd";
    
        // prepare the query
        $stmt = $this->conn->prepare($query);
    
        // sanitize
        $this->username=htmlspecialchars(strip_tags($this->username));
        $this->pswd=htmlspecialchars(strip_tags($this->pswd));
    
        // bind the values
        $stmt->bindParam(':username', $this->username);
        // hash the password before saving to database
        $password_hash = password_hash($this->pswd, PASSWORD_BCRYPT);
        $stmt->bindParam(':pswd', $password_hash);
    
        // execute the query, also check if query was successful
        if(!$this->usernameExists() && $stmt->execute()){
            return true;
        }
    
        return false;
    }

        // check if given username exist in the database
    function usernameExists(){
    
        // query to check if username exists
        $query = "SELECT id, username, pswd
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
    
            // return true because username exists in the database
            return true;
        }
    
        // return false if username does not exist in the database
        return false;
    }
 
    // update a user record
    public function update(){
        if($this->usernameExists()) {
            // if password needs to be updated
            //$password_set=!empty($this->pswd) ? ", pswd = :pswd" : "";
            $password_set = !empty($this->pswd) ? "SET pswd = :pswd" : "";
        
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

}

?>
