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

const video = document.querySelector(".video");

function playVideo(){
    if (video.paused || video.ended) {
    video.play();
    } else {
    video.pause();
    }
}


//function PlayModuleVideo(s){
//    document.getElementById("vdosrc").src = {{ "module.class_"+s+"_video.url" }};
//    document.getElementById("vdoname").innerHTML = {{ "module.class_"+s+"_name" }};
//}
