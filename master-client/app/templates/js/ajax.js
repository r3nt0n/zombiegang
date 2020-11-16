<script>

function is_proxy_enabled(destCheck, host, port) {
    $.post('{{ url_for('ajax_bp.is_proxy_enabled') }}').done(function(response) {
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

function toggle_proxy(destCheck, host, port, destErrElem) {
    $.post('{{ url_for('ajax_bp.toggle_proxy') }}',
        {
            host: encodeURI(document.getElementById(host).value),
            port: encodeURI(document.getElementById(port).value)
        }).done(function(response) {
        is_proxy_enabled(destCheck, host, port);
    }).fail(function() {
        is_proxy_enabled(destCheck, host, port);
        $(destErrElem).text("error: could not contact server");
        $(destErrElem).css("display", "inline");
    });
}

function get_actual_ip(destElemIP, destElemCC, destElemFlag) {
    $(destElemIP).html('㊗️'); // loading icon
    $.post('{{ url_for('ajax_bp.get_actual_ip') }}').done(function(response) {
        $(destElemIP).text(response['ip']), $(destElemCC).text(response['country']), $(destElemFlag).text(response['flag'])
    }).fail(function() {
        $(destElemIP).text("error: could not contact server");
        $(destElemIP).css("color", "red");
    });
}

function json_export(data_type, data) {
    console.log(data);
    var checkboxes = $('input[name="'+ data_type + '_checked"]');
    var $checked = checkboxes.filter(":checked"),
        checkedValues = $checked.map(function () {
            return this.value;
        }).get();
    $.post('{{ url_for('ajax_bp.json_export') }}',
        {
            data_type: data_type,
            data: JSON.stringify(data),
            data_checked: JSON.stringify(checkedValues)
        }).done(function(response) {
        location.href = response['url'];
    }).fail(function() {
        //pass
    });
}

</script>