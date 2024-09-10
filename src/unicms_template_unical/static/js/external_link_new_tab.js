//open external link in new tab
document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll("a[href^=http]");
    [].forEach.call(links, function(l) {
        if(l.getAttribute("href").indexOf(location.hostname) == -1) {
            l.setAttribute("target", "_blank");
            //l.setAttribute("rel", "noreferrer noopener");
            //use Django SECURE_REFERRER_POLICY
            l.setAttribute("rel", "noopener");
        }
   })
});
