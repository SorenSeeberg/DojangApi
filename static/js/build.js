function handleSignIn() {
    console.log("Sign in !");
    var email = document.getElementById('input-field-email').value;
    var password = document.getElementById('input-field-password').value;
    var formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    fetch("/users/sign-in", {
        body: formData,
        method: "post"
    }).then(function (response) {
        if (response.status == 200) {
            console.log('Du er nu logget ind');
        }
        else if (response.status == 401) {
            console.log('Email og/eller password er forkert!');
        }
        return response.json();
    }).then(function (myJson) {
        console.log(myJson);
    });
}
function signIn() {
    var template = document.getElementById('handlebars-sign-in-form').innerHTML;
    var templateScript = Handlebars.compile(template);
    var context = { "name": "Ritesh Kumar", "occupation": "developer" };
    var html = templateScript(context);
    var articleElement = document.getElementById('article');
    articleElement.innerHTML = html;
}
function componentHeader(loggedIn) {
    if (loggedIn === void 0) { loggedIn = true; }
    var title = "Dojang";
    var headerElement = document.getElementById('header');
    if (loggedIn) {
        headerElement.innerHTML = "<div>" + title + "</div><div class='header-profile'/>";
    }
    else {
        headerElement.innerHTML = "<div>" + title + "</div>";
    }
    signIn();
}
function componentSignIn() {
    var articleElement = document.getElementById('article');
}
//# sourceMappingURL=build.js.map