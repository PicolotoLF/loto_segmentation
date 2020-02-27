function formataDinheiro(n) {
     document.write("R$ " + n.toFixed(2).replace('.', ',').replace(/(\d)(?=(\d{3})+\,)/g, "$1."));
}

function calculateSegments(){
    showNotification('top','center', 'info', 'Calculating Segments...')
    $.ajax(
        {url: "/task_calculate", success: function(result){
                showNotification('top','center', 'success', 'Complete Calculated Segments')
            }
        }
    );

}

function showNotification(from, align, color, message) {
    type = ['primary', 'info', 'success', 'warning', 'danger'];
//    color = Math.floor((Math.random() * 4) + 1);

    $.notify({
      icon: "tim-icons icon-bell-55",
      message: message

    }, {
      type: color,
      timer: 8000,
      placement: {
        from: from,
        align: align
      }
    });
  }
