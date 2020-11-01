Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}

NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = this.length - 1; i >= 0; i--) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

function toggleMinimize(elementid) {
  var x = document.getElementById(elementid);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}


function toggle_checkall(source, checkboxes_name) {
  checkboxes = document.getElementsByName(checkboxes_name);
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}


function enable_fields(checkbox, fields) {
  checkbox = document.getElementById(checkbox);
  fields.forEach(field_id => {
    var input = document.getElementById(field_id);
    if(checkbox.checked){
      input.disabled = false;
      input.focus();
    }
    else{
      input.disabled=true;
    }
  });
}