function refreshPage()
{
	if(window.scrollY == 0)
		window.location = window.location.href;
}
var interval = 5*1000;
setTimeout(setInterval('refreshPage()', interval),interval);
console.log("auto_refresher.js loaded");
console.log("Scroll down to stop refreshing page");