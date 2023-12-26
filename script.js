//determines if a click in a td node is made on a link, if so don't mark the event as selected
var onLink = false;
var darkMode = false;
var showGrid = true;

if(document.cookie){
	temp = document.cookie.split(";");
	for(i = 0; i < temp.length; i++){
		if(temp[i].split("=")[0].trim() == "darkMode"){
			//console.log(temp[i].split("=")[0].trim());
			//console.log(temp[i].split("=")[1].trim());
			if(temp[i].split("=")[1].trim() == "true"){
				toggleItems("darkMode");
				document.getElementById("darkModeInput").checked = true;
			}
			else{
				darkMode = false;
				document.getElementById("darkModeInput").checked = false;
			}
		}
		else if(temp[i].split("=")[0].trim() == "showGrid"){
			if(temp[i].split("=")[1].trim() == "false"){
				toggleItems("grid");
				document.getElementById("gridInput").checked = false;
			}
			else{
				document.getElementById("gridInput").checked = true;
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

function toggleDarkMode(){
	toggleItems("darkMode");
}

function toggleGrid(){
	toggleItems("grid");
}

function toggleItems(toggleItem){
	if(toggleItem == "darkMode"){
		if(darkMode){
			darkMode = false;
		}
		else{
			darkMode = true;
		}
	}
	else if(toggleItem == "grid"){
		if(showGrid){
			showGrid = false;
		}
		else{
			showGrid = true;
		}
	}
	if(darkMode){
		document.body.setAttribute("class", "bodycolor-darkMode");
	}
	else{
		document.body.setAttribute("class", "bodycolor-lightMode");
	}
	ths = document.getElementsByTagName("TH");
	for(th in ths){
		if(ths[th].nodeType == Node.ELEMENT_NODE){
			if(darkMode){
				ths[th].setAttribute("class", "something-darkMode");
			}
			else{
				ths[th].setAttribute("class", "something");
			}
		}
	}
	tds = document.getElementsByTagName("TD");
	for(td in tds){
		if(tds[td].nodeType == Node.ELEMENT_NODE){
			if(tds[td].dataset.selected == "selected"){
				if(darkMode && showGrid){
					tds[td].setAttribute("class", "something-selected-darkMode");
				}
				else if(darkMode && !showGrid){
					tds[td].setAttribute("class", "something-selected-darkMode-noGrid");
				}
				else if(!darkMode && showGrid){
					tds[td].setAttribute("class", "something-selected-noGrid");
				}
				else{
					tds[td].setAttribute("class", "something-selected");
				}
			}
			else{
				if(darkMode && showGrid){
					tds[td].setAttribute("class", "something-darkMode");
				}
				else if(darkMode && !showGrid){
					tds[td].setAttribute("class", "something-darkMode-noGrid");
				}
				else if(!darkMode && showGrid){
					tds[td].setAttribute("class", "something");
				}
				else{
					tds[td].setAttribute("class", "something-noGrid");
				}
			}
		}
	}
	mores = document.querySelectorAll("a.more-darkMode");
	//console.log(mores);
	for(more in mores){
		if(mores[more] != undefined && mores[more].nodeType == Node.ELEMENT_NODE){
			if(darkMode){
				mores[more].setAttribute("class", "more-darkMode");
			}
			else{
				mores[more].setAttribute("class", "more-lightMode");
			}
		}
	}
	links = document.querySelectorAll("a.link-darkMode");
	//console.log(links);
	for(link in links){
		if(links[link] != undefined && links[link].nodeType == Node.ELEMENT_NODE){
			if(darkMode){
				links[link].setAttribute("class", "link-darkMode");
			}
			else{
				links[link].setAttribute("class", "link-lightMode");
			}
		}
	}
	tmp = document.cookie;
	document.cookie = "showGrid=" + showGrid + ";darkMode=" + darkMode + ";expires=;path=/;" + tmp;
}

//function to toggle, if an event has been selected
function toggleClick(thisObject, init){
	if(thisObject.dataset.selected == "unselected" && !onLink){
		if(darkMode){
			thisObject.setAttribute("class", "something-selected-darkMode");
		}
		else{
			thisObject.setAttribute("class", "something-selected");
		}
		thisObject.dataset.selected = "selected";
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
		if(darkMode){
			thisObject.setAttribute("class", "something-darkMode");
		}
		else{
			thisObject.setAttribute("class", "something");
		}
		thisObject.dataset.selected = "unselected";
		//remove the id from the cookie
		temp = document.cookie.split(";");
		for(i = 0; i < temp.length; i++){
			if(temp[i].split("=")[0].trim() == "events"){
				document.cookie = "events=" + temp[i].split("=")[1].replace(thisObject.getAttribute("id") + "$", "") + ";" + "$;expires=" + dayAfter + ";path=/;";
			}
		}
	}
}