
function myFunction() {
    document.getElementById("open_zach").classList.toggle("show");
    document.getElementById("button_color").classList.toggle("show_color");
}

window.onclick = function(event) {
    if (!event.target.matches('.button_zach')) {
      var dropdowns = document.getElementsByClassName("zach_content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
      var dropdowns_ = document.getElementsByClassName("zach_header");
      var j;
      for (j = 0; j < dropdowns_.length; j++) {
        var openDropdown_ = dropdowns_[j];
        if (openDropdown_.classList.contains('show_color')) {
          openDropdown_.classList.remove('show_color');
        }
      }
    }
  }


