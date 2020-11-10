<?php
function post_request($url, $data, $content_type='json'){
    //$data = array ('foo' => 'bar', 'bar' => 'baz');
    if ($data) {
    $data = http_build_query($data);
    }

    if ($content_type == 'https') {
        $content_type = "Content-type: application/x-www-form-urlencoded\r\n";
    }
    elseif ($content_type == 'json') {
        $content_type = "Content-type: application/json\r\n";
    }

    $context_options = array (
            'http' => array (
                'method' => 'POST',
                'header'=> $content_type . "Content-Length: " . strlen($data) . "\r\n",
                'content' => $data
                )
            );

    $context = stream_context_create($context_options);
    // enable https in prd enviroments
    //$proto = 'https://';
    //$url = $proto . $url;
    try{
        $fp = fopen($url, 'r', false, $context);    
        // header information as well as meta data
        // about the stream
        //var_dump(stream_get_meta_data($stream));
        // actual data at $url
        $data_recv = stream_get_contents($stream);
        fclose($stream);

        return $data_recv;
    }
    catch (Exception $e){
        return False;
    }
}
?>