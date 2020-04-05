function playPause(ele, but) {
	
    var myVideo = document.getElementById(ele)
    if (myVideo.paused) {
      myVideo.play();
      // but.innerHTML = "Pause";
      if (but.classList.contains('fa-play-circle')) {
          but.classList.toggle('fa-play-circle')
        but.classList.add('fa-pause-circle')
      }
      else {
          but.classList.add('fa-pause-circle')
      }
  
      }
    else { 
      myVideo.pause();
      // but.innerHTML = "Play";
      but.classList.remove('fa-pause-circle');
      but.classList.add('fa-play-circle');
      }
  } 