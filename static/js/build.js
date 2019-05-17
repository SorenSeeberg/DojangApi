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
        historyRouter({ data: null, title: '', url: routeNames.signIn });
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateSignIn();
    }
    else {
        historyRouter({ data: null, title: '', url: routeNames.frontPage });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateMainMenu();
    }
}
function pageCreateUser() {
    if (!getAccessToken()) {
        historyRouter({ data: null, title: '', url: routeNames.createUser });
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateCreateUser();
    }
    else {
        pageIndex();
    }
}
function pageInfo(context) {
    historyRouter({ data: null, title: '', url: '' });
    templateTopBarSignedOut(TITLE_CONTEXT);
    templateInfo(context);
}
function pageInfo401() {
    pageInfo({ message: "<h1>401 Unauthorized</h1>", buttonAction: "pageIndex()", buttonText: "Til forsiden" });
}
function pageInfo404() {
    pageInfo({ message: "<h1>404 Not Found</h1>", buttonAction: "pageIndex()", buttonText: "Til forsiden" });
}
function pageLoading(loggedIn) {
    if (loggedIn === void 0) { loggedIn = true; }
    loggedIn
        ? templateTopBarSignedIn(TITLE_CONTEXT)
        : templateTopBarSignedOut(TITLE_CONTEXT);
    templateLoading();
}
function pageQuizCategory() {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, title: '', url: routeNames.quizCategory });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizCategory();
    }
}
function pageQuizConfig(config) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, title: '', url: routeNames.quizConfig });
        handleGetQuizConfiguration();
    }
}
var _a;
var routeNames = {
    index: '/',
    signIn: '/log-ind',
    frontPage: '/forside',
    createUser: '/opret-bruger',
    quizCategory: '/quiz-category',
    quizConfig: '/quiz-configuration',
    curriculum: '/pensum'
};
var routes = (_a = {},
    _a[routeNames.index] = pageIndex,
    _a[routeNames.signIn] = pageIndex,
    _a[routeNames.frontPage] = pageIndex,
    _a[routeNames.createUser] = pageCreateUser,
    _a[routeNames.curriculum] = pageIndex,
    _a[routeNames.quizCategory] = pageQuizCategory,
    _a[routeNames.quizConfig] = pageQuizConfig,
    _a);
function spaRouter() {
    console.log('spaRouter');
    console.log(window.location.pathname);
    console.log(routes);
    routes[window.location.pathname]();
}
function historyRouter(url) {
    console.log('historyRouter');
    console.log(url);
    console.log(routes);
    history.pushState(url.data, url.title, url.url);
}
function setTemplate(templateId, contentTarget, context) {
    if (context === void 0) { context = {}; }
    var template = document.getElementById(templateId).innerHTML;
    var templateScript = Handlebars.compile(template);
    var html = templateScript(context);
    var contentContainer = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}
function templateQuizCategory() {
    setTemplate("handlebars-quiz-category", "article");
}
function templateQuizConfig(config) {
    var select = [];
    console.log('templateQuizConfig');
    console.log(config);
    Object.keys(config).forEach(function (k) {
        if (k !== 'displayNames') {
            select.push("<label>" + config['displayNames'][k] + "</label><select>" + config[k].map(function (o) { return "<option>" + o + "</option>"; }).join('') + "</select>");
        }
    });
    setTemplate("handlebars-quiz-configuration", "article", { select: select.join('') });
}
function templateMainMenu() {
    setTemplate("handlebars-main-menu", "article");
}
function templateSignIn(context) {
    setTemplate('handlebars-sign-in-form', "article", context);
}
function templateCreateUser() {
    setTemplate('handlebars-create-user', "article");
}
function templateInfo(context) {
    setTemplate('handlebars-info', "article", context);
}
function templateTopBarSignedIn(context) {
    setTemplate("handlebars-top-bar-signed-in", "header", context);
}
function templateTopBarSignedOut(context) {
    setTemplate("handlebars-top-bar-signed-out", "header", context);
}
function templateLoading() {
    setTemplate('handlebars-loading', 'article');
}
var ACCESS_TOKEN_KEY = 'accessToken';
var QUIZ_TOKEN_KEY = 'quizToken';
function getAuthorizationHeader() {
    var headers = new Headers();
    headers.append('Authorization', getAccessToken());
    return headers;
}
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
        var email, password, response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    email = document.getElementById('input-field-email');
                    password = document.getElementById('input-field-password');
                    templateLoading();
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
                    templateSignIn({
                        message: '<p class="clr-error">Email og/eller password er ikke korrekt</p>',
                        extra: '<button class="btn btn-link" type="button" onclick="pageCreateUser()">Glemt password?</button>'
                    });
                    return [2, false];
            }
        });
    });
}
function handleCreateUser() {
    return __awaiter(this, void 0, void 0, function () {
        var email, password, passwordRepeat, formData, response, responseObject, message;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    email = document.getElementById('input-field-email');
                    password = document.getElementById('input-field-password');
                    passwordRepeat = document.getElementById('input-field-password-repeat');
                    if (!email) {
                        pageInfo({
                            message: "Du skal indtaste en email",
                            buttonAction: 'pageCreateUser()',
                            buttonText: 'Create User'
                        });
                        return [2];
                    }
                    if (password.value !== passwordRepeat.value) {
                        pageInfo({
                            message: "Passwords skal være forskelige",
                            buttonAction: 'pageCreateUser()',
                            buttonText: 'Create User'
                        });
                        return [2];
                    }
                    if (!password.value || !passwordRepeat.value) {
                        pageInfo({
                            message: "Du skal indtaste et password",
                            buttonAction: 'pageCreateUser()',
                            buttonText: 'Create User'
                        });
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
                        message = "<p>Tillykke!</p><p>Vi har nu oprettet din nye profil. Nu mangler du blot at aktivere den" +
                            " via det link jeg netop har send til dig :)</p><br><p>Med venlig hilsen,</p><p>Grand Master Kwon!</p>";
                        pageInfo({ message: message, buttonText: 'Til Log Ind', buttonAction: 'pageIndex()' });
                        return [2, true];
                    }
                    pageInfo({
                        message: "Emailen er allerede optaget. Måske har du glemt dit password?",
                        buttonAction: 'pageCreateUser()',
                        buttonText: 'Create User'
                    });
                    return [2, false];
            }
        });
    });
}
function handleGetQuizConfiguration() {
    return __awaiter(this, void 0, void 0, function () {
        var response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    templateLoading();
                    return [4, fetch('/quiz/configuration', {
                            method: "get",
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        templateTopBarSignedIn(TITLE_CONTEXT);
                        templateQuizConfig(responseObject.body);
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        pageInfo401();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
function handleCreateNewQuiz() {
    return __awaiter(this, void 0, void 0, function () {
        var quiz, response, responseObject, quiz_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    quiz = {
                        categoryId: 2,
                        levelMin: 3,
                        levelMax: 8,
                        questionCount: 25,
                        optionCount: 3,
                        timeLimit: 10
                    };
                    templateLoading();
                    return [4, fetch('/quiz', {
                            method: "post",
                            body: JSON.stringify(quiz),
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 201) {
                        quiz_1 = responseObject.body;
                        setQuizToken(quiz_1.quizToken);
                        pageInfo({ message: 'Yep', buttonAction: 'pageIndex()', buttonText: 'Hell Yes!' });
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        pageInfo401();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
//# sourceMappingURL=build.js.map