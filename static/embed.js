function render_git_stats() {
	fetch('http://127.0.0.1:5000/gitstat/'+window.git_stat_config.usr_id, {mode: 'cors'})
		.then(
			function (response) {
				if (response.status !== 200) {
					console.log('Looks like there was a problem. Status Code: ' +
						response.status);
					return;
				}

				response.text().then(function (data) {
					let my_frame = document.createElement("iframe");
					my_frame.srcdoc = data;
					let div = document.getElementById("git_stats");
					div.appendChild(my_frame);
				});
			}
		)
		.catch(function (err) {
			console.log('Fetch Error :-S', err);
		});
};
