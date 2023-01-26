$(document).ready(function () {
	$(".messages").animate({ scrollTop: $(".messages ul").height() }, "slow");
	// rest of the script
	try {
		const roomName = JSON.parse(
			document.getElementById("room-name").textContent
		);
		if (roomName) {
			loadRoom(roomName);
		}
	} catch (error) {
		console.log(error.message);
	}
});

$("#profile-img").click(function () {
	$("#status-options").toggleClass("active");
});

$(".expand-button").click(function () {
	$("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function () {
	$("#profile-img").removeClass();
	$("#status-online").removeClass("active");
	$("#status-away").removeClass("active");
	$("#status-busy").removeClass("active");
	$("#status-offline").removeClass("active");
	$(this).addClass("active");

	if ($("#status-online").hasClass("active")) {
		$("#profile-img").addClass("online");
	} else if ($("#status-away").hasClass("active")) {
		$("#profile-img").addClass("away");
	} else if ($("#status-busy").hasClass("active")) {
		$("#profile-img").addClass("busy");
	} else if ($("#status-offline").hasClass("active")) {
		$("#profile-img").addClass("offline");
	} else {
		$("#profile-img").removeClass();
	}

	$("#status-options").removeClass("active");
});

function newMessage(message, sender) {
	if ($.trim(message) == "") {
		return false;
	}
	try {
		const userEmail = JSON.parse(
			document.getElementById("user-email").textContent
		);
		if (userEmail === sender) {
			$(
				'<li class="sent"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' +
					message +
					"</p></li>"
			).appendTo($(".messages ul"));
		} else {
			$(
				'<li class="replies"><img src="http://emilcarlsson.se/assets/mikeross.png" alt="" /><p>' +
					message +
					"</p></li>"
			).appendTo($(".messages ul"));
		}
	} catch (error) {
		console.log(error.message);
	}

	$(".message-input input").val(null);
	// $(".contact.active .preview").html("<span>You: </span>" + message);
	$(".messages").animate({ scrollTop: $(".messages ul").height() }, "fast");
}

function loadRoom(roomName) {
	const chatSocket = new WebSocket(
		"ws://" + window.location.host + "/ws/chat/" + roomName + "/"
	);

	chatSocket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		newMessage(data.message, data.sender);
	};

	chatSocket.onclose = function (e) {
		console.error("Chat socket closed unexpectedly");
	};

	$(".message-input input").focus();

	$(".submit").click(function () {
		var msgInput = $(".message-input input");
		const message = msgInput.val();
		chatSocket.send(
			JSON.stringify({
				message: message,
			})
		);
	});

	$(window).on("keydown", function (e) {
		if (e.which == 13) {
			$(".submit").click();
		}
	});
}
$(".contact").click(function (e) {
	let room = $(this).data("room");
	$.ajax({
		type: "get",
		url: room,
	})
		.success(function (data) {
			window.location.href = window.location.origin + "/chat/" + data;
		})
		.fail(function (data) {
			alert(data);
			console.log(data);
		});
});
