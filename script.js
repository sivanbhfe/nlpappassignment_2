function changeContent(page) {
	var maincontentDiv = document.getElementById('maincontent')
	var universContent = document.getElementById('universe')
	switch (page) {
		case 'home':
			maincontentDiv.innerHTML = '<h1>Add, View and Update Knowledge Graph</h1>'
			break;
		default:
			maincontentDiv.innerHTML = '<h2>Page not found!</h2>';
	}
}

function runsentimentanalysis() {
	var textinput = document.getElementById('inputtextarea').value;
	stringifiedlisttextarea = JSON.stringify(textinput);
	const containertable2 = document.getElementById("repeatinput");
	formatted2 = '<span>';
	formatted2  += textinput;
	formatted2  += '</span>';
	containertable2.innerHTML = "";
	containertable2.innerHTML = formatted2;
			// a POST request
	const response = fetch('http://127.0.0.1:5000/sentimentanalysis', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlisttextarea)
	}).then((response) => response.text())
  .then((response) => {
    const containertable = document.getElementById("resultarea");
	containertable.innerHTML=""
	formatted = '<span id="sentimentoutput">';
	formatted  += response;
	formatted  += '</span>';
   	containertable.innerHTML += "The sentiment category for the above text is: " + formatted;
	const containertable3 = document.getElementById("sentimentoutput");
	containertable3.setAttribute("Value",response);
	  });
			// a POST request
	const responseimg = fetch('http://127.0.0.1:5000/sentimentscoreandvisual', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlisttextarea)
	}).then((responseimg) => responseimg.blob())
	.then((blob) => {
	const imageUrl = URL.createObjectURL(blob);
	const imageElement = document.createElement("img");
	imageElement.src = imageUrl;
	const container = document.getElementById("graphdisplayarea");
	container.innerHTML=""
	container.appendChild(imageElement);
		});
}


function readSingleFile (evt) {

	var f = evt.target.files[0];
	if (f) {
	var r = new FileReader();
	r.onload = function(e) {
	var contents = e.target.result;
	var lines = contents
	const containertable = document.getElementById("resultarea");
	const containertable2 = document.getElementById("repeatinput");
	formatted2 = '<span>';
	formatted2  += contents;
	formatted2  += '</span>';
	containertable2.innerHTML = "";
	containertable2.innerHTML = formatted2;
	// formatted = '<span>';
	// formatted  += lines;
	// formatted  += '</span>';
   	// containertable.innerHTML = formatted;

	stringifiedlistfileupload = JSON.stringify(lines);
			// a POST request
	const response = fetch('http://127.0.0.1:5000/sentimentanalysis', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlistfileupload)
	}).then((response) => response.text())
  .then((response) => {
    const containertable = document.getElementById("resultarea");
	containertable.innerHTML=""
	formatted = '<span id="sentimentoutput">';
	formatted  += response;
	formatted  += '</span>';
	containertable.innerHTML += "The sentiment category for the above text is: " + formatted;
	const containertable3 = document.getElementById("sentimentoutput");
	containertable3.setAttribute("Value",response);

	  });

			// a POST request
	const responseimg = fetch('http://127.0.0.1:5000/sentimentscoreandvisual', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlistfileupload)
	}).then((responseimg) => responseimg.blob())
	.then((blob) => {
	const imageUrl = URL.createObjectURL(blob);
	const imageElement = document.createElement("img");
	imageElement.src = imageUrl;
	const container = document.getElementById("graphdisplayarea");
	container.innerHTML=""
	container.appendChild(imageElement);
		});
	}
	r.readAsText(f);
	document.getElementById("fileinput").value=""
	} else { 
	alert("Failed to load file");
	}
}



function refresh(){
	location.reload();
}
