var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var TITLE_CONTEXT = { title: 'Dojang' };
function pageIndex() {
    if (!getAccessToken()) {
        scilentRoute({ data: null, title: '', url: 'sign-in' });
        componentTopBarSignedOut(TITLE_CONTEXT);
        componentSignIn();
    }
    else {
        scilentRoute({ data: null, title: '', url: 'welcome' });
        componentTopBarSignedIn(TITLE_CONTEXT);
        componentMainMenu();
    }
}
function pageCreateUser() {
    if (!getAccessToken()) {
        scilentRoute({ data: null, title: 'Hello', url: 'create-user' });
        componentTopBarSignedOut(TITLE_CONTEXT);
        componentCreateUser();
    }
    else {
        pageIndex();
    }
}
function pageCreatedUserSuccess() {
    scilentRoute({ data: null, title: '', url: '' });
    componentTopBarSignedOut(TITLE_CONTEXT);
    componentCreatedUser();
}
function pageLoading(loggedIn) {
    if (loggedIn === void 0) { loggedIn = true; }
    loggedIn
        ? componentTopBarSignedIn(TITLE_CONTEXT)
        : componentTopBarSignedOut(TITLE_CONTEXT);
    templateLoading();
}
var routes = {
    '/': pageIndex,
    '/sign-in': pageIndex,
    '/welcome': pageIndex,
    '/create-user': pageCreateUser,
    '/curriculum': ''
};
function handleRoute() {
    console.log('pathname');
    console.log(window.location.pathname);
    routes[window.location.pathname]();
}
function scilentRoute(url) {
    var values = Object.keys(url).map(function (k) { return url[k]; }).slice();
    console.log(values);
    history.replaceState(url.data, url.title, url.url);
}
function setTemplate(templateId, contentTarget, context) {
    if (context === void 0) { context = {}; }
    var template = document.getElementById(templateId).innerHTML;
    var templateScript = Handlebars.compile(template);
    var html = templateScript(context);
    var contentContainer = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}
function componentMainMenu() {
    setTemplate("handlebars-main-menu", "article");
}
function componentSignIn() {
    setTemplate('handlebars-sign-in-form', "article");
}
function templateSignInError() {
    setTemplate('handlebars-sign-in-form-error', "article");
}
function componentCreateUser() {
    setTemplate('handlebars-create-user', "article");
}
function componentCreatedUser() {
    setTemplate('handlebars-created-user', "article");
}
function componentTopBarSignedIn(context) {
    setTemplate("handlebars-top-bar-signed-in", "header", context);
}
function componentTopBarSignedOut(context) {
    setTemplate("handlebars-top-bar-signed-out", "header", context);
}
function templateLoading() {
    setTemplate('handlebars-loading', 'article');
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
function handleSignIn() {
    return __awaiter(this, void 0, void 0, function () {
        var email, password, formData, response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    email = document.getElementById('input-field-email');
                    password = document.getElementById('input-field-password');
                    templateLoading();
                    formData = new FormData();
                    formData.append('email', email.value);
                    formData.append('password', password.value);
                    return [4, fetch('/users/sign-in', {
                            body: formData,
                            method: "post"
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        setAccessToken(responseObject.body.accessToken);
                        pageIndex();
                        return [2, true];
                    }
                    templateSignInError();
                    return [2, false];
            }
        });
    });
}
function handleCreateUser() {
    return __awaiter(this, void 0, void 0, function () {
        var email, password, passwordRepeat, formData, response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    email = document.getElementById('input-field-email');
                    password = document.getElementById('input-field-password');
                    passwordRepeat = document.getElementById('input-field-password-repeat');
                    if (password.value !== passwordRepeat.value) {
                        return [2];
                    }
                    pageLoading(false);
                    formData = new FormData();
                    formData.append('email', email.value);
                    formData.append('password', password.value);
                    return [4, fetch('/users', {
                            body: formData,
                            method: "post"
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 201) {
                        pageCreatedUserSuccess();
                        return [2, true];
                    }
                    return [2, false];
            }
        });
    });
}
//# sourceMappingURL=build.js.map