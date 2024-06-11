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
function PlayModuleVideo(s){
    document.getElementById("vdosrc").src = "{{ module.class_"+s+"_video.url }}";
    document.getElementById("vdoname").innerHTML = "{{ module.class_"+s+"_name }}";
}





