//determines if a click in a td node is made on a link, if so don't mark the event as selected
var onLink = false;

if(document.cookie){
	temp = document.cookie.split(";");
	for(i = 0; i < temp.length; i++){
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

//function to toggle, if an event has been selected
function toggleClick(thisObject, init){
	if(thisObject.title == "unselected" && !onLink){
		thisObject.style.backgroundColor = "Gray";
		thisObject.style.color = "White";
		thisObject.title = "selected";
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
	}else if(thisObject.title == "selected" && !onLink){
		thisObject.style.backgroundColor = "White";
		thisObject.style.color = "Gray";
		thisObject.title = "unselected";
		//remove the id from the cookie
		temp = document.cookie.split(";");
		for(i = 0; i < temp.length; i++){
			if(temp[i].split("=")[0].trim() == "events"){
				document.cookie = "events=" + temp[i].split("=")[1].replace(thisObject.getAttribute("id") + "$", "") + ";" + "$;expires=" + dayAfter + ";path=/;";
			}
		}
	}
}