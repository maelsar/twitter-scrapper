
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
