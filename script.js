//determines if a click in a td node is made on a link, if so don't mark the event as selected
var onLink = false;

document.getElementById("darkModeInput").addEventListener("click", function(){toggleItems("darkMode");});
document.getElementById("gridInput").addEventListener("click", function(){toggleItems("grid");});

if(document.cookie){
	temp = document.cookie.split(";");
	for(i = 0; i < temp.length; i++){
		if(temp[i].split("=")[0].trim() == "darkMode"){
			if(temp[i].split("=")[1].trim() == "true"){
				document.getElementById("darkModeInput").checked = true
				toggleItems("darkMode");
			}
		}
		else if(temp[i].split("=")[0].trim() == "showGrid"){
			if(temp[i].split("=")[1].trim() == "false"){
				toggleItems("grid");
			}
			else{
				document.getElementById("gridInput").checked = true
			}
		}
		else{
			if(temp[i].split("=")[0].trim() == "events"){
				events = temp[i].split("=")[1].split("$");
				for(j = 0; j < events.length - 1; j++){
					if(document.getElementById(events[j]) == null){
						console.log("Couldn't find event with ID " + events[j] + ", might be an old event remaining in cookie from earlier events");
					}else{
						toggleClick(document.getElementById(events[j]), true);
					}
				}
			}
		}
	}
}

//
function getCookieItem(term){
	items = document.cookie.split(";");
	for(i = 0; i < items.length; i++){
		if(items[i].split("=")[0] == term){
			return items[i].split("=")[1];
		}
	}
	return "";
}

function updateTD(elem){
	if(elem.nodeType == Node.ELEMENT_NODE){
		if(elem.getAttribute("class").includes("nothing")){
				if(document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "nothing-darkMode");
				}
				else if(document.getElementById("darkModeInput").checked && !document.getElementById("gridInput").checked){
					elem.setAttribute("class", "nothing-darkMode-noGrid");
				}
				else if(!document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "nothing");
				}
				else{
					elem.setAttribute("class", "nothing-noGrid");
				}
		}
		else{
			if(elem.dataset.selected == "selected"){
				if(document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something-selected-darkMode");
				}
				else if(document.getElementById("darkModeInput").checked && !document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something-selected-darkMode-noGrid");
				}
				else if(!document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something-selected-noGrid");
				}
				else{
					elem.setAttribute("class", "something-selected");
				}
			}
			else{
				if(document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something-darkMode");
				}
				else if(document.getElementById("darkModeInput").checked && !document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something-darkMode-noGrid");
				}
				else if(!document.getElementById("darkModeInput").checked && document.getElementById("gridInput").checked){
					elem.setAttribute("class", "something");
				}
				else{
					elem.setAttribute("class", "something-noGrid");
				}
			}
		}
	}
}

function toggleItems(toggleItem){
	if(document.getElementById("darkModeInput").checked){
		document.body.setAttribute("class", "bodycolor-darkMode");
	}
	else{
		document.body.setAttribute("class", "bodycolor-lightMode");
	}
	ths = document.getElementsByTagName("TH");
	for(th in ths){
		if(ths[th].nodeType == Node.ELEMENT_NODE){
			if(document.getElementById("darkModeInput").checked){
				ths[th].setAttribute("class", "something-darkMode");
			}
			else{
				ths[th].setAttribute("class", "something");
			}
		}
	}
	tds = document.getElementsByTagName("TD");
	for(td in tds){
		updateTD(tds[td]);
	}
	mores = document.querySelectorAll("a.more-darkMode");
	//console.log(mores);
	for(more in mores){
		if(mores[more] != undefined && mores[more].nodeType == Node.ELEMENT_NODE){
			if(document.getElementById("darkModeInput").checked){
				mores[more].setAttribute("class", "more-darkMode");
			}
			else{
				mores[more].setAttribute("class", "more-lightMode");
			}
		}
	}
	links = document.querySelectorAll("a");
	//console.log(links);
	for(link in links){
		if(links[link] != undefined && links[link].nodeType == Node.ELEMENT_NODE){
			if(document.getElementById("darkModeInput").checked){
				links[link].setAttribute("class", "link-darkMode");
			}
			else{
				links[link].setAttribute("class", "link-lightMode");
			}
		}
	}
	document.cookie = "showGrid=" + document.getElementById("gridInput").checked + ";max-age=31536000" + ";path=/";
	document.cookie = "darkMode=" + document.getElementById("darkModeInput").checked + ";max-age=31536000" + ";path=/";
}

//function to toggle, if an event has been selected
function toggleClick(thisObject, init){
	if(thisObject.dataset.selected == "unselected" && !onLink){
		thisObject.dataset.selected = "selected";
		updateTD(thisObject);
		//if this is not the initialization, add the event to the cookie
		if(!init){
			//add the id of this event to the cookie
			temp = document.cookie.split(";");
			events = "";
			for(i = 0; i < temp.length; i++){
				if(temp[i].split("=")[0].trim() == "events"){
					events += temp[i].split("=")[1];
				}
			}
			document.cookie = "events=" + events + thisObject.getAttribute("id") + "$;expires=" + dayAfter + ";path=/;";
		}
	}
	else if(thisObject.dataset.selected == "selected" && !onLink){
		thisObject.dataset.selected = "unselected";
		updateTD(thisObject);
		//remove the id from the cookie
		temp = document.cookie.split(";");
		for(i = 0; i < temp.length; i++){
			if(temp[i].split("=")[0].trim() == "events"){
				document.cookie = "events=" + temp[i].split("=")[1].replace(thisObject.getAttribute("id") + "$", "") + ";" + "$;max-age=31536000;path=/;";
			}
		}
	}
}