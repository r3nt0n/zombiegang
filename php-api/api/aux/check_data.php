<?php

function starts_with($string, $query){
    return substr($string, 0, strlen($query)) === $query;
}

function ends_with($string, $query){
    $length = strlen($query);
    return substr($string, -$length, $length) === $query;
  }

?>