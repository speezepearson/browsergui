document.addEventListener('change', function(event){event.target.dispatchEvent(new Event('input'))});
document.addEventListener('propertychange', function(event){event.target.dispatchEvent(new Event('input'))});

function obey(command) {
  if (command) {
    console.log("evaluating:", command);
    try {
      eval(command);
    } catch (e) {
      window.close();
      // If a second window is opened, something funny happens and obey() is given some HTML as its command.
      // There's a syntax error, and we reach this block of code.
      // JS may keep running after calling window.close(), causing another request to /command to be make
      // and thereby stealing the command meant for the other window.
      // Re-raising the error will stop the request from being made.
      throw e;
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
