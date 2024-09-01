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

let Str_txt=[]
function addrelationship() {
	var fentity = document.getElementById('firstentity').value;
	var relationship = document.getElementById('relationship').value;
	var sentity = document.getElementById('secondentity').value;
if (relationship != "select") {
	// if (Str_txt.length != 0) {
		const container1 = document.getElementById("queriedsubgraph");
		container1.innerHTML=""
		var temp = 0
	for (let i = 0; i < Str_txt.length; i++) {
		console.log(Str_txt[i]["fentity"])
		if (Str_txt[i]["fentity"] == fentity && Str_txt[i]["sentity"] == sentity ){
			Str_txt[i]["fentity"] = fentity;
			Str_txt[i]["sentity"] = sentity;
			Str_txt[i]["relationship"] = relationship
			temp = 1
			break;
		} 
	}

	if (temp == 0) {
			Str_txt.push({"fentity":fentity,"relationship":relationship,"sentity":sentity});
		}
	
	if (Str_txt.length == 0) {
		console.log("HEEREEE")
		Str_txt.push({"fentity":fentity,"relationship":relationship,"sentity":sentity});
	}
// } else {
// 	Str_txt.push({"fentity":fentity,"relationship":relationship,"sentity":sentity});	
// }

	console.log("STRTX"+Str_txt)
	stringifiedlist = JSON.stringify(Str_txt);
	console.log(Str_txt)
			// a POST request
	const response = fetch('http://127.0.0.1:5000/addrelationship', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlist)
	}).then((response) => response.blob())
  .then((blob) => {
    const imageUrl = URL.createObjectURL(blob);
    const imageElement = document.createElement("img");
    imageElement.src = imageUrl;
    const container = document.getElementById("knowledgegraphdisplayarea");
	container.innerHTML=""
    container.appendChild(imageElement);
	  });
	  
	  
	const containertable = document.getElementById("knowledgegraphtable");
	var out=''
	for(let items of Str_txt){
      out += `
	          <tr>
            <td>${items.fentity}</td>
            <td>${items.relationship}</td>
            <td>${items.sentity}</td>
         </tr>
	      `;
   }
	formatted = '<tr><th>First Entity</th><th>Relationship</th><th>Second Entity</th></tr>';
	formatted  += out;
   containertable.innerHTML = formatted;
}	else {
	window.alert("Please select a valid relationship");
}
}

function entityquery() {

	var entityquery = document.getElementById('entityquery').value;
	var url = "http://127.0.0.1:5000/entityquery/"
	var url2 = url+entityquery
	const response1 = fetch(url2, {
		method: 'POST',
		contentType: 'application/json',
		body: JSON.stringify(stringifiedlist)
		}).then((response) => response.blob())
  .then((blob) => {
    const imageUrl = URL.createObjectURL(blob);
    const imageElement = document.createElement("img");
    imageElement.src = imageUrl;
    const container = document.getElementById("queriedsubgraph");
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
		var lines = contents.split("\r\n");
		console.log(lines.length)
		for (var i=1; i<lines.length-1; i++){
			let text = lines[i].split(",");
			Str_txt.push({"fentity":text[0],"relationship":text[1],"sentity":text[2]});
		}
	const containertable = document.getElementById("knowledgegraphtable");
	var out=''
	for(let items of Str_txt){
      out += `
	          <tr>
            <td>${items.fentity}</td>
            <td>${items.relationship}</td>
            <td>${items.sentity}</td>
         </tr>
	      `;
   }
	formatted = '<tr><th>First Entity</th><th>Relationship</th><th>Second Entity</th></tr>';
	formatted  += out;
   	containertable.innerHTML = formatted;
	console.log("STRT"+Str_txt.length)

	stringifiedlist = JSON.stringify(Str_txt);
	console.log(Str_txt)
			// a POST request
	const response = fetch('http://127.0.0.1:5000/addrelationship', {
	method: 'POST',
	contentType: 'application/json',
	body: JSON.stringify(stringifiedlist)
	}).then((response) => response.blob())
  .then((blob) => {
    const imageUrl = URL.createObjectURL(blob);
    const imageElement = document.createElement("img");
    imageElement.src = imageUrl;
    const container = document.getElementById("knowledgegraphdisplayarea");
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
