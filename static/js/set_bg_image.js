/*
 * Initializes background image functionality for elements with the class 'img-container'.
 * 
 * Upon DOMContentLoaded:
 * - Selects all elements with the class 'img-container' using `querySelectorAll`.
 * - Iterates over each `container` element in the `imgContainers` collection.
 * - Retrieves the `data-bg-image` attribute from each container, which contains the URL of the background image.
 * - If a `data-bg-image` attribute is found:
 *   - Sets the container's `backgroundImage` style property to the value of the `data-bg-image` attribute.
 */
document.addEventListener("DOMContentLoaded", function() {
    var imgContainers = document.querySelectorAll('.img-container');
    imgContainers.forEach(function(container) {
      var bgImage = container.getAttribute('data-bg-image');
      if (bgImage) {
        container.style.backgroundImage = 'url(' + bgImage + ')';
      }
    });
  });
  