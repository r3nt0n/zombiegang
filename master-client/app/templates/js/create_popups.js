
<script>
function create_proxy_popup(sourceElem) {
  sourceElem = document.getElementById(sourceElem);
  var popup = document.createElement('DIV');   // Create a <button> element
  popup.innerHTML = `{% include ('objects/windows/popups/proxy.html') %}`;
  sourceElem.appendChild(popup);
  get_actual_ip('#actual-ip', '#proxy-country', '#proxy-flag');
  is_proxy_enabled('proxy-enabled', 'proxy_host', 'proxy_port');
}

</script>