// function render_git_stats() {
// 	fetch('http://127.0.0.1:5000/gitstat/'+window.git_stats_config.usr_id, {mode: 'cors'})
// 		.then(
// 			function (response) {
// 				if (response.status !== 200) {
// 					console.log('Looks like there was a problem. Status Code: ' +
// 						response.status);
// 					return;
// 				}

// 				response.text().then(function (data) {
// 					let my_frame = document.createElement("iframe");
// 					// let doc = my_frame.contentWindow.document;
// 					my_frame.getElementsByTagName(body).append(data)
// 					// doc.open();
// 					// doc.write(data);
// 					// doc.close();
// 					my_frame.id = "git-stats-embeded";
// 					let div = document.getElementById("git_stats");
// 					div.appendChild(my_frame);


// 					let my_frame_style = document.createElement("style");
// 					let css = "iframe {border:none; width: 100%; height:100%; overflow:hidden;}";
// 					my_frame_style.appendChild(document.createTextNode(css));

// 					document.head.append(my_frame_style);
// 				});
// 			}
// 		)
// 		.catch(function (err) {
// 			console.log('Fetch Error :-S', err);
// 		});
// };

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function render_git_stats() {
	let my_frame = document.createElement("iframe");
	my_frame.src = 'http://127.0.0.1:5000/gitstat/'+ getCookie("GitStatUsr")
	my_frame.id = "git-stats-embeded";
	let div = document.getElementById("git_stats");
	div.appendChild(my_frame);


	let my_frame_style = document.createElement("style");
	let css = "iframe {border:none; width: 100%; height:100%; overflow:hidden;}";
	my_frame_style.appendChild(document.createTextNode(css));

	document.head.append(my_frame_style);
}
document.load = render_git_stats();
