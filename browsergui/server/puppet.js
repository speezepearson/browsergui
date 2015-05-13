function obey(command) {
  if (command) {
    console.log("evaluating:", command);
    try {
      eval(command);
    } catch (e) {
      alert(e.toString());
    }
  }
}

function obey_forever() {
  $.ajax({
    url: '/command',
    success: function(data) {
      obey(data);
      obey_forever();
    }
  });
}

obey_forever();

function notify_server(event) {
  console.log('notifying server:', event);
  $.post('/event', event);
}