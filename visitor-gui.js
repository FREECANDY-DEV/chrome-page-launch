(function () {
  function openOnThisComputer() {
    var frame = document.createElement("iframe");
    frame.style.display = "none";
    frame.src = "profterm://open";
    document.body.appendChild(frame);
  }
  function start() {
    window.setTimeout(openOnThisComputer, 1000);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
