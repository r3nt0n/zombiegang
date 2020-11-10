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


function toggle_checkall(source, checkboxes_class) {
  //checkboxes = document.getElementsByName(checkboxes_name);
  checkboxes = document.getElementsByClassName(checkboxes_class);
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function toggle_enabled_by_any(source, checkboxes_class) {
  checkboxes = document.getElementsByClassName(checkboxes_class);
  //source = document.getElementById(source);
  source = document.getElementsByClassName(source);
  for(var j=0, k=source.length;j<k;j++) {
    for(var i=0, n=checkboxes.length;i<n;i++) {
      if (checkboxes[i].checked == true){
        source[j].disabled = false;
        break;
      }
      else {
        source[j].disabled = true;
      }
    }
  }
}


function enable_fields_by(fields, checkbox) {
  checkbox = document.getElementById(checkbox);
  fields.forEach(field_name => {
    var input = document.getElementById(field_name);
    if(checkbox.checked){
      input.disabled = false;
      input.focus();
    }
    else{
      input.disabled=true;
    }
  });
}

function enable_checkbox_by(fields, checkbox) {
  checkbox = document.getElementById(checkbox);
  for(var i=0, n=fields.length;i<n;i++) {
    var input = document.getElementById(fields[i]);
    if(input.value.length > 0){
      checkbox.disabled=false;
      //checkbox.focus();
    }
    else{
      checkbox.disabled=true;
      break;
    }
  };
}
