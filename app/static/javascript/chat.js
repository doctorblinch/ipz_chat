$(document).ready(function() {
	var socket = io.connect('http://192.168.128.34:5000');
	socket.on('connect', function() {
		socket.send(' has connected!');
	});
	socket.on('message', function(msg) {
		//console.log('Received message' + msg);

		console.log(msg);
		msg[1] = msg[1]
			.replace('<','&lt;')
			.replace('>', '&gt;');
		$("#messages").append('<li>🐊' + '<small>(' + msg[2] + ')</small> ' + '<b>' + msg[0] + '</b>: ' + msg[1] + '</li>');
		console.log(msg[0] + ' send: ' + msg[1]);
		text_for_scroll = document.getElementById("myMessage");
		//text_for_scroll.scrollTop = 9999;
		//text_for_scroll.scrollIntoView();
	});
	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		console.log($('#myMessage').val());
		$('#myMessage').val('');
	});
});
