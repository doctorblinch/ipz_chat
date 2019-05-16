
$(document).ready(function() {
	ip = 'http://' + '192.168.0.101' + ':5000';
	var socket = io.connect(ip);
	socket.on('connect', function() {
		socket.send(' has connected!');
	});
	socket.on('message', function(msg) {

		console.log(msg);
		msg[1] = msg[1]
			.replace('<','&lt;')
			.replace('>', '&gt;');
		$("#messages").append('<li>🐊' + '<small>(' + msg[2] + ')</small> ' + '<b>' + msg[0] + '</b>: ' + msg[1] + '</li>');
		console.log(msg[0] + ' send: ' + msg[1]);
		//getElementById('messages').scrollTop = 1000;
		//let text_for_scroll = document.getElementById("messages");
		//text_for_scroll.scrollTop = 9999;
		//text_for_scroll.scrollIntoView();
		//console.log('dsddss'+text_for_scroll);
		//text_for_scroll.scrollTop = text_for_scroll.scrollHeight;
	});
	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		console.log($('#myMessage').val());
		$('#myMessage').val('');
	});
});
