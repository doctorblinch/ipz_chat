$(document).ready(function() {
	ip = 'http://' + '192.168.32.228' + ':5000';
	var socket = io.connect(ip);
	socket.on('connect', function() {
		pathname = window.location.pathname
		let for_send = [' has connected!',pathname]
		socket.send(for_send);
	});

	socket.on('message', function(msg) {
		console.log(msg);
		msg[1] = msg[1]
			.replace('<','&lt;')
			.replace('>', '&gt;');
		$("#messages").append('<p>🐊' + '<small>(' + msg[2] + ')</small> ' + '<b>' + msg[0] + '</b>: ' + msg[1] + '</p>');
		console.log(msg[0] + ' send: ' + msg[1]);
		});

	$('#sendbutton').on('click', function() {
		if ($('#myMessage').val() != ''){
			pathname = window.location.pathname
			let for_send = [$('#myMessage').val(),pathname]
			socket.send(for_send);
			console.log($('#myMessage').val());
			$('#myMessage').val('');
	}
		});


		$('#sendvoice').on('click', function() {
				pathname = window.location.pathname
				let for_send = ['voice message',pathname]
				socket.send(for_send);
				console.log('Voice!!!');
				$('#myMessage').val('');
			});

		function sendMsg(key){
		    switch(key.keyCode){
		        case 13:
						if ($('#myMessage').val() != ''){
							pathname = window.location.pathname
							let for_send = [$('#myMessage').val(),pathname]
							socket.send(for_send);
							console.log($('#myMessage').val());
							$('#myMessage').val('');
						}
		    }
		}

		addEventListener("keypress", sendMsg);
});
