//determines if a click in a td node is made on a link, if so don't mark the event as selected
var onLink = false;
var darkMode = false;
var darkModeBackground = "Black";
var darkModeText = "White";
var darkModeSelectedEvent = "DarkGray";
var lightModeBackground = "White";
var lightModeText = "Black";
var lightModeSelectedEvent = "LightGray";

if(document.cookie){
	temp = document.cookie.split(";");
	for(i = 0; i < temp.length; i++){
		if(temp[i].split("=")[0].trim() == "darkMode"){
			//console.log(temp[i].split("=")[0].trim());
			//console.log(temp[i].split("=")[1].trim());
			if(temp[i].split("=")[1].trim() == "true"){
				toggleDarkMode();
			}else{
				darkMode = false;
			}
		}else{
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
	if(darkMode){
		darkMode = false;
		document.body.setAttribute("class", "bodycolor-lightMode");
		ths = document.getElementsByTagName("TH");
		for(th in ths){
			if(ths[th].nodeType == Node.ELEMENT_NODE){
				ths[th].setAttribute("class", "something");
			}
		}
		tds = document.getElementsByTagName("TD");
		for(td in tds){
			if(tds[td].nodeType == Node.ELEMENT_NODE){
				if(tds[td].dataset.selected == "selected"){
					tds[td].setAttribute("class", "something-selected");
				}else{
					tds[td].setAttribute("class", "something");
				}
			}
		}
		mores = document.querySelectorAll("a.more-darkMode");
		console.log(mores)
		for(more in mores){
			if(mores[more] != undefined && mores[more].nodeType == Node.ELEMENT_NODE){
				mores[more].setAttribute("class", "more-lightMode");
			}
		}
		links = document.querySelectorAll("a.link-darkMode");
		console.log(links)
		for(link in links){
			if(links[link] != undefined && links[link].nodeType == Node.ELEMENT_NODE){
				links[link].setAttribute("class", "link-lightMode");
			}
		}
		tmp = document.cookie;
		document.cookie = tmp.replace("darkMode=true;", "darkMode=false;");
	}else{
		darkMode = true;
		document.body.setAttribute("class", "bodycolor-darkMode");
		ths = document.getElementsByTagName("TH");
		for(th in ths){
			if(ths[th].nodeType == Node.ELEMENT_NODE){
				ths[th].setAttribute("class", "something-darkMode");
			}
		}
		tds = document.getElementsByTagName("TD");
		for(td in tds){
			if(tds[td].nodeType == Node.ELEMENT_NODE){
				if(tds[td].dataset.selected == "selected"){
					tds[td].setAttribute("class", "something-selected-darkMode");
				}else{
					tds[td].setAttribute("class", "something-darkMode");
				}
			}
		}
		mores = document.querySelectorAll("a.more-lightMode");
		console.log(mores)
		for(more in mores){
			if(mores[more] != undefined && mores[more].nodeType == Node.ELEMENT_NODE){
				mores[more].setAttribute("class", "more-darkMode");
			}
		}
		links = document.querySelectorAll("a.link-lightMode");
		console.log(links)
		for(link in links){
			if(links[link] != undefined && links[link].nodeType == Node.ELEMENT_NODE){
				links[link].setAttribute("class", "link-darkMode");
			}
		}
		tmp = document.cookie;
		document.cookie = "darkMode=true;expires=;path=/;" + tmp;
	}
}

//function to toggle, if an event has been selected
function toggleClick(thisObject, init){
	if(thisObject.dataset.selected == "unselected" && !onLink){
		if(darkMode){
			thisObject.setAttribute("class", "something-selected-darkMode");
		}else{
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
	}else if(thisObject.dataset.selected == "selected" && !onLink){
		if(darkMode){
			thisObject.setAttribute("class", "something-darkMode");
		}else{
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