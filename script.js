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
			// a POST request
	const response = fetch('http://127.0.0.1:5000/sentimentanalysis', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlisttextarea)
	}).then((response) => response.text())
  .then((response) => {
    const datafetched = response
    const containertable = document.getElementById("resultarea");
	formatted = '<span>';
	formatted  += datafetched;
	formatted  += '</span>';
   	containertable.innerHTML = formatted;
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
    const datafetched = response
    const containertable = document.getElementById("resultarea");
	formatted = '<span>';
	formatted  += datafetched;
	formatted  += '</span>';
   	containertable.innerHTML = formatted;
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
