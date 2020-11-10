<script>

function is_proxy_enabled(destCheck, host, port) {
    $.post('{{ url_for('is_proxy_enabled') }}').done(function(response) {
      let check_input = document.getElementById(destCheck);
      let host_input = document.getElementById(host);
      let port_input = document.getElementById(port);
      if (response['enabled'] == 'true') {
        check_input.checked = true;
        host_input.value = response['host'];
        port_input.value = response['port'];
        enable_checkbox_by(['proxy_host', 'proxy_port'], 'proxy-enabled');
      }
      else {
        check_input.checked = false;
        host_input.value = '';
        port_input.value = '';
        enable_checkbox_by(['proxy_host', 'proxy_port'], 'proxy-enabled');
      }
    }).fail(function() {
        check_input.checked = false;
        host_input.value = '';
        port_input.value = '';
        enable_checkbox_by(['proxy_host', 'proxy_port'], 'proxy-enabled');
    });
}

function toggle_proxy(destCheck, host, port) {
    $.post('{{ url_for('toggle_proxy') }}',
        {
            host: encodeURI(document.getElementById(host).value),
            port: encodeURI(document.getElementById(port).value)
        }).done(function(response) {
        is_proxy_enabled(destCheck, host, port);
    }).fail(function() {
        //pass
    });
}

function get_actual_ip(destElemIP, destElemCC, destElemFlag) {
    $(destElemIP).html('㊗️'); // loading icon
    $.post('{{ url_for('get_actual_ip') }}').done(function(response) {
        $(destElemIP).text(response['ip']), $(destElemCC).text(response['country']), $(destElemFlag).text(response['flag'])
    }).fail(function() {
        $(destElem).text("error: could not contact server");
    });
}

</script>