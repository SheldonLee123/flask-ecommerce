function agree_terms() {
      var box = document.getElementById("inlineRadioOptions");
      if(box.checked==true)
        document.getElementById("complete").disabled = false;
      else
        document.getElementById("complete").disabled = true;
    }
