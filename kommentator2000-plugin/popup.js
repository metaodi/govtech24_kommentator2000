
console.log("popup.js loaded");
document.getElementById("title-h1").textContent = "Kommentator 2000";
document.getElementById("download-btn").addEventListener("click", function(e) {
  document.getElementById("title-h1").textContent = "Kommentator 2000, it's a go.";


  
  chrome.runtime.sendMessage({'myPopupIsOpen': true});

});