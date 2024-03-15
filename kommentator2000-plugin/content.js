console.log("started");

chrome.runtime.onMessage.addListener(function(message, sender) {

  alert("ping");

  newUrl = "http://127.0.0.1:5000?consultation_id="+document.getElementsByClassName('srnummer')[0].textContent;
  chrome.tabs.create({ url: newURL });


});