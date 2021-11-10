function setItemInSession(id, dict) {
    sessionStorage.setItem(window.location.href + "@" + id,
                           JSON.stringify(dict))
}
