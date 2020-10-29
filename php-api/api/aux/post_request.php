<?php
function post_request($url, $data){
    //$data = array ('foo' => 'bar', 'bar' => 'baz');
    $data = http_build_query($data);

    $context_options = array (
            'http' => array (
                'method' => 'POST',
                'header'=> "Content-type: application/x-www-form-urlencoded\r\n"
                    . "Content-Length: " . strlen($data) . "\r\n",
                'content' => $data
                )
            );

    $context = stream_context_create($context_options);
    
    $proto = 'http://';
    // enable https in prd enviroments
    //$proto = 'https://';
    $url = $proto . $url;
    $fp = fopen($url, 'r', false, $context);
}
?>