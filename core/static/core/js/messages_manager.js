/**
 * Surface Django messages injected in #django-messages (embedded + website shells).
 */
(function () {
  function showMessages() {
    var root = document.getElementById("django-messages");
    if (!root) {
      return;
    }
    var nodes = root.querySelectorAll("[data-content]");
    nodes.forEach(function (el) {
      var text = el.getAttribute("data-content");
      if (!text) {
        return;
      }
      var isError = el.getAttribute("data-error") === "1";
      if (typeof shopify !== "undefined" && shopify.toast && shopify.toast.show) {
        shopify.toast.show(text, { isError: isError, duration: 5000 });
      }
    });
    root.remove();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showMessages);
  } else {
    showMessages();
  }
})();
