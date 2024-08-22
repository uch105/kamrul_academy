//navbar js----------------

let openHam = document.querySelector('#openHam');
let closeHam = document.querySelector('#closeHam');
let navigationItems = document.querySelector('#navigation-items');

const hamburgerEvent = (navigation, close, open) => {
    navigationItems.style.display = navigation;
    closeHam.style.display = close;
    openHam.style.display = open;
};

openHam.addEventListener('click', () => hamburgerEvent("flex", "block", "none"));
closeHam.addEventListener('click', () => hamburgerEvent("none", "none", "block"));




var progress = document.getElementById("progress").value

document.getElementById("progressbar").style.width = `${progress}%`;


function PlayModuleVideo(s){
    class_name = "class_"+s+"_name"
    class_video = "class_"+s+"_video"
    document.getElementById("vdosrc").src = document.getElementById(class_video).innerText;
    document.getElementById("vdoname").innerHTML = document.getElementById(class_name).innerText;
    document.getElementsByTagName("video")[0].load();
}