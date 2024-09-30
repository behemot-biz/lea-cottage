document.addEventListener("DOMContentLoaded", function() {
    var imgContainers = document.querySelectorAll('.img-container');
    imgContainers.forEach(function(container) {
      var bgImage = container.getAttribute('data-bg-image');
      if (bgImage) {
        container.style.backgroundImage = 'url(' + bgImage + ')';
      }
    });
  });
  