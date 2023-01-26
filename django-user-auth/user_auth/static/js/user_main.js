$(document).ready(function () {
	loginCheck();
});
/**
 * Check if the user is authenticated on page load.
 * If the user is authenticated, display a warning toast and redirect the user back to the previous page.
 * If the previous page cannot be found, redirect the user to the homepage.
 */
function loginCheck() {
	let check = $("#login-check");
	if (check.data("authenticated") === true) {
		let homeUrl = $("#home-url").data("url");
		setTimeout(() => {
			createToast(
				"Warning",
				"You are already logged in, redirecting ",
				"warning",
				() => {
					if (document.referrer) {
						window.history.back();
					} else {
						window.location.href = homeUrl;
					}
				}
			);
		}, 1000);
	}
}

function clearForm() {
	var formErrors = document.querySelectorAll(".invalid-feedback");
	formErrors.forEach((element) => {
		element.remove();
	});
}
function submitForm(currId, formData, actionUrl, fMethod) {
	$.ajax({
		type: fMethod,
		url: actionUrl,
		data: formData,
		success: function (response) {
			if (response.status == "error") {
				// display error messages

				for (var key in response.errors) {
					if (currId === "login-form") {
						if (key === "__all__") {
							createToast(
								"Error",
								response.errors[key],
								response.status
							);
						} else {
							var input = $("#log" + key);
							input.addClass("is-invalid");
							input.after(
								"<div class='invalid-feedback'>" +
									response.errors[key] +
									"</div>"
							);
						}
					} else if (currId === "register-form") {
						if (key === "__all__") {
							createToast(
								"Error",
								response.errors[key],
								response.status
							);
						} else {
							var input = $("#reg" + key);
							input.addClass("is-invalid");
							input.after(
								"<div class='invalid-feedback'>" +
									response.errors[key] +
									"</div>"
							);
						}
					}
				}
			} else if (response.status == "success") {
				if (currId === "login-form") {
					createToast(
						"Success",
						"You were logged in successfully, redirecting",
						response.status,
						redirectToPreviousPage
					);
				} else {
					createToast(
						"Success",
						"Account has been added successfully",
						response.status,
						redirectToPreviousPage
					);
				}
			} else {
				createToast(
					"Error",
					"Something went wrong, please try again",
					"warning"
				);
				// redirect user to the page they came from or to the specified success url
			}
		},
		error: function (error) {
			createToast(
				"Error",
				"Something went wrong, please try again",
				"warning"
			);
		},
	});
}

$("form").submit(function (e) {
	e.preventDefault(); // prevent the form from submitting
	// Check if the form is either or login or registration form
	// If it is we intercept and handle the submission, otherwise we let it go
	var currId = $(this).attr("id");
	if (currId === "login-form" || currId === "register-form") {
		var formData = $(this).serialize();
		var actionUrl = $(this).attr("action");
		var fMethod = $(this).attr("method");
		clearForm();
		submitForm(currId, formData, actionUrl, fMethod);
	} else {
		$(this).off("submit").submit();
	}
});

function createToast(
	heading,
	text,
	icon,
	after = function () {
		return false;
	}
) {
	if (!after()) {
		$.toast({
			text: text,
			heading: heading,
			showHideTransition: "slide",
			icon: icon,
		});
	} else {
		let delay = 2000;
		$.toast({
			text: text,
			heading: heading,
			showHideTransition: "slide",
			icon: icon,
			hideAfter: delay, // delay in milliseconds
			afterHidden: function () {
				setTimeout(after, delay);
			},
		});
	}
}

function redirectToPreviousPage() {
	var homeUrl = $("#home-url").data("url");
	setTimeout(() => {
		if (document.referrer) {
			window.history.back();
		} else {
			window.location.href = homeUrl;
		}
	}, 3000);
}

