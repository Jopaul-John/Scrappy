 
        $(document).ready(function () {
            // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
            $('.modal').modal();
            $('.modal1').modal();
            $('.carousel').carousel();
            $('.slider').slider({
                full_width: true
            });
            $('.slider').slider('pause');
            autoplay()

            function autoplay() {
                $('.slider').slider('next');
                setTimeout(autoplay, 2000);
            }
        });

        function initMap() {
            var uluru = {
                lat: 10.1782,
                lng: 76.4305
            };
            var map = new google.maps.Map(document.getElementById('map'), {
                zoom: 15,
                center: uluru,
                 zoomControl: false,
                scaleControl: false,
                scrollwheel: false,
                disableDoubleClickZoom: true,
            });
            var marker = new google.maps.Marker({
                position: uluru,
                map: map
            });
        }

        particlesJS("particles-js", {
  "particles": {
    "number": {
      "value": 100,
      "density": {
        "enable": true,
        "value_area": 1000
      }
    },
    "color": {
      "value": "#009EFF"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#009EFF"
      },
      "polygon": {
        "nb_sides": 2
      },
      "image": {
        "src": "images/tathva-man.png",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 1,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 10,
        "opacity_min": 0.5,
        "sync": false
      }
    },
    "size": {
      "value": 3,
      "random": true,
      "anim": {
        "enable": true,
        "speed": 6,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 75,
      "color": "#009EFF",
      "opacity": 1,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 3,
      "direction": "random",
      "random": true,
      "straight": false,
      "out_mode": "out",
      "bounce": false,
      "attract": {
        "enable": true,
        "rotateX": 60000,
        "rotateY": 12000
      }
    }
  },
  "interactivity": {
    "detect_on": "window",
    "events": {
      "onhover": {
        "enable": true,
        "mode": "grab"
      },
      "onclick": {
        "enable": true,
        "mode": "repulse"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 140,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 400,
        "size": 40,
        "duration": 2,
        "opacity": 8,
        "speed": 3
      },
      "repulse": {
        "distance": 200,
        "duration": 0.4
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true
});

 new WOW().init();

   $(function(){
      $("#sub_title").typed({
        strings: ["Let's Get Rid of your Scrap", "Via Online"],
        typeSpeed: 50,
        loop: true,
      });
 
      $("#main_title").typed({
        strings: ["Scrappy"],
        typeSpeed: 50,
        loop: false,
         showCursor: false
      });
  });

   (function($){
  $(function(){

     $('.button-collapse').sideNav();
       $('.parallax').parallax();
       $('.scrollspy').scrollSpy({
          scrollOffset: 45
        });

       $('.carousel').carousel();
        

  });  
})(jQuery); 


   


