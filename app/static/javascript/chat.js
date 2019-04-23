$(document).ready(function() {
	var socket = io.connect('http://192.168.131.14:5000');
	socket.on('connect', function() {
		socket.send(' has connected!');
	});
	socket.on('message', function(msg) {
		//console.log('Received message' + msg);
		$("#messages").append('<li>'+ msg[0] + 'send:' + msg[1] + '</li>');
		//$("#messages").append('<p>eeeee' +msg[0]+ '<p>');
		console.log(msg[0] + 'send:' + msg[1]);
	});
	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		console.log($('#myMessage').val());
		$('#myMessage').val('');
	});
});
