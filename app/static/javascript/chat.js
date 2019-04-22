$(document).ready(function() {
	var socket = io.connect('http://192.168.131.201:5000');
	socket.on('connect', function() {
		socket.send('User has connected!');
	});
	socket.on('message', function(msg) {
		$("#messages").append('<li>'+msg+'</li>');
		console.log('Received message' + msg);
	});
	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		console.log($('#myMessage').val());
		$('#myMessage').val('');
	});
});
