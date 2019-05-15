function setTemplate(templateId, contentTarget, context) {
    if (context === void 0) { context = {}; }
    var template = document.getElementById(templateId).innerHTML;
    var templateScript = Handlebars.compile(template);
    var html = templateScript(context);
    var contentContainer = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}
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
        if (response.status === 200) {
            console.log('Du er nu logget ind');
        }
        else if (response.status === 401) {
            console.log('Email og/eller password er forkert!');
        }
        return response.json();
    }).then(function (responseObject) {
        if (responseObject.status === 200) {
            setAccessToken(responseObject.body.accessToken);
            pageIndex();
        }
        console.log(responseObject);
    });
}
function componentMainMenu() {
    setTemplate("handlebars-main-menu", "article");
}
function componentSignIn() {
    setTemplate('handlebars-sign-in-form', "article");
}
function componentTopBarSignedIn(context) {
    setTemplate("handlebars-top-bar-signed-in", "header", context);
}
function componentTopBarSignedOut(context) {
    setTemplate("handlebars-top-bar-signed-out", "header", context);
}
var routes = {
    '': pageIndex,
    '/': pageIndex,
    '/sign-in': pageIndex,
    '/menu': pageIndex,
    '/curriculum': ''
};
function handleRoute() {
    console.log('pathname');
    console.log(window.location.pathname);
    routes[window.location.pathname]();
}
function pageIndex() {
    var context = { title: "Dojang" };
    if (!getAccessToken()) {
        componentSignIn();
        componentTopBarSignedOut(context);
    }
    else {
        componentMainMenu();
        componentTopBarSignedIn(context);
    }
}
var ACCESS_TOKEN_KEY = 'accessToken';
var QUIZ_TOKEN_KEY = 'quizToken';
function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}
function setAccessToken(token) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
}
function clearAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
}
function getQuizToken() {
    return localStorage.getItem(QUIZ_TOKEN_KEY);
}
function setQuizToken(token) {
    localStorage.setItem(QUIZ_TOKEN_KEY, token);
}
function clearQuizToken() {
    localStorage.removeItem(QUIZ_TOKEN_KEY);
}
//# sourceMappingURL=build.js.map