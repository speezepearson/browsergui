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
  var request = new XMLHttpRequest();
  request.open('get', '/command');
  request.onload = function() {
    obey(this.responseText);
    obey_forever();
  }
  request.send();
}

obey_forever();

function notify_server(event) {
  console.log('notifying server:', event);
  var request = new XMLHttpRequest();
  request.open('post', '/event');
  request.send(JSON.stringify(event));
}
