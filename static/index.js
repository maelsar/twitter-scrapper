function isChecked() {
  if(document.getElementById("return5").checked){
    document.getElementById("return1").disabled = true;
    document.getElementById("return1").checked = false;
    document.getElementById("return2").disabled = true;
    document.getElementById("return2").checked = false;
    document.getElementById("return3").disabled = true;
    document.getElementById("return3").checked = false;
    document.getElementById("return4").disabled = true;
    document.getElementById("return4").checked = false;
  }
  else {
    document.getElementById("return1").disabled = false;
    document.getElementById("return2").disabled = false;
    document.getElementById("return3").disabled = false;
    document.getElementById("return4").disabled = false;
  }
}

var clicked = false;
for (i = 0; i <= 4; i++) {
  if($('#return'+[i]).is(':checked'))  {
    clicked = true;
    return;
  }
}
if(clicked == false) {
  document.getElementById("return"+[1]).checked;
  document.getElementById("return"+[2]).checked;
  document.getElementById("return"+[3]).checked;
  document.getElementById("return"+[4]).checked;
}
