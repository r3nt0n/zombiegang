<?php
function concat_fields_with_commas($fields){
    $columns_to_set = "";
    foreach ($fields as $field => $value) {
        if (!empty($field)) {
            if (!empty($columns_to_set)) { $columns_to_set = $columns_to_set . ', ';}  // add comma between args
            $columns_to_set = $columns_to_set .  $value ." = :" . $value;
        }
    }
    unset($value);
    return $columns_to_set;
}

//function concat_fields_with_and($fields){
//}

?>