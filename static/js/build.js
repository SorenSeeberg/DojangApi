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
var infoBoxErrorLevel = {
    info: 'info-box',
    error: 'info-box error',
    success: 'info-box success'
};
function pageInfo(context) {
    historyRouter({ data: null, title: '', url: '' });
    templateTopBarSignedOut(TITLE_CONTEXT);
    templateInfo(context);
}
function pageInfo401() {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "401 Unauthorized",
        message: "",
        buttonAction: "pageIndex()",
        buttonText: "Til forsiden"
    });
}
function pageInfo404() {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "404 Not Found",
        message: "",
        buttonAction: "pageIndex()",
        buttonText: "Til forsiden"
    });
}
function pageInfoNotImplemented() {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "Not Implemented",
        message: "På vej",
        buttonAction: "pageIndex()",
        buttonText: "Til forsiden"
    });
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
function pageQuiz(quiz) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        var options = quiz.currentQuestion.options.map(function (o) { return "<button class=\"btn btn-large-wide btn-secondary\" type=\"button\" onclick=\"handleAnswerQuestion(" + o.index + ")\">" + o.option + "</button>"; }).join('');
        var context = {
            percentageComplete: Math.round(quiz.currentQuestionIndex / quiz.totalQuestions * 100),
            progressBarText: quiz.currentQuestionIndex + " / " + quiz.totalQuestions,
            category: quiz.title,
            question: quiz.currentQuestion.question,
            options: options
        };
        historyRouter({ data: quiz.quizToken, title: '', url: routeNames.quiz });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuiz(context);
    }
}
function pageQuizResult(result) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, title: '', url: routeNames.result + "/" + result.quizToken });
        var star = '&#10026;';
        var stars = result.percentageCorrect === 100
            ? "<h1 class=\"gold-font star\">" + star + " " + star + " " + star + "</h1><p>Perfekt</p>"
            : result.percentageCorrect >= 90
                ? "<h1 class=\"silver-font star\">" + star + " " + star + "</h1><p>Flot pr\u00E6station</p>"
                : result.percentageCorrect >= 75
                    ? "<h1 class=\"bronze-font star\">" + star + "</h1><p>Du klarede den lige</p>"
                    : '<h3 class="runner-up-font">Ikke bestået</h3><p>Wax on  . . was off . .</p>';
        var minutes = Math.floor(result.timeSpent / 60);
        var seconds = Math.floor(result.timeSpent - (minutes * 60));
        var timeSpent = minutes + ":" + (seconds > 9 ? seconds : "0" + seconds);
        var context = {
            category: "" + result.categoryName,
            stars: stars,
            percentageCorrect: result.percentageCorrect,
            timeSpent: timeSpent,
            answers: result.answers.map(function (a, i) { return "<p class=\"" + (a.correct ? '' : 'error') + "\">" + (i + 1) + ". " + a.text + "</p>"; }).join('')
        };
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizResult(context);
    }
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
function handleCreateNewQuiz(quizConfig) {
    if (quizConfig === void 0) { quizConfig = quizConfigTemp; }
    return __awaiter(this, void 0, void 0, function () {
        var response, responseObject, quiz;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    templateLoading();
                    return [4, fetch('/quiz', {
                            method: "post",
                            body: JSON.stringify(quizConfig),
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 201) {
                        quiz = responseObject.body;
                        console.log(quiz);
                        setQuizToken(quiz.quizToken);
                        pageQuiz(quiz);
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
function handleGetResult() {
    return __awaiter(this, void 0, void 0, function () {
        var quizToken, response, responseObject, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    quizToken = getQuizToken();
                    return [4, fetch("/quiz/result/" + quizToken, {
                            method: "get",
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        result = responseObject.body;
                        pageQuizResult(result);
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
function handleGetQuiz() {
    return __awaiter(this, void 0, void 0, function () {
        var quizToken, response, responseObject, quiz;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    quizToken = getQuizToken();
                    return [4, fetch("/quiz/" + quizToken, {
                            method: "get",
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (!(responseObject.status === 200)) return [3, 6];
                    quiz = responseObject.body;
                    if (!!responseObject.body.complete) return [3, 3];
                    pageQuiz(quiz);
                    return [3, 5];
                case 3:
                    console.log('Complete!');
                    pageLoading();
                    return [4, handleGetResult()];
                case 4:
                    _a.sent();
                    _a.label = 5;
                case 5: return [2, true];
                case 6:
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
function handleClearQuiz() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2];
        });
    });
}
function handleAnswerQuestion(optionIndex) {
    return __awaiter(this, void 0, void 0, function () {
        var quizToken, response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    quizToken = getQuizToken();
                    return [4, fetch("/quiz/question/" + quizToken, {
                            method: 'put',
                            body: JSON.stringify({ optionIndex: optionIndex }),
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (!(responseObject.status === 200)) return [3, 6];
                    console.log(responseObject);
                    if (!(responseObject.body.answer === true)) return [3, 4];
                    console.log('Korrekt');
                    return [4, handleGetQuiz()];
                case 3:
                    _a.sent();
                    return [3, 5];
                case 4:
                    console.log('Forkert');
                    pageInfo({
                        title: 'Svaret er forkert',
                        message: responseObject.body.text,
                        errorLevel: infoBoxErrorLevel.error,
                        buttonText: 'Næste spørgsmål',
                        buttonAction: 'handleGetQuiz()'
                    });
                    _a.label = 5;
                case 5: return [2, true];
                case 6:
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
var quizConfigTemp = {
    categoryId: 2,
    levelMin: 3,
    levelMax: 8,
    questionCount: 5,
    optionCount: 3,
    timeLimit: 10
};
var quizConfig1Dan = {
    questionCount: 25,
    optionCount: 3,
    levelMin: 1,
    levelMax: 11,
    categoryId: 0,
    timeLimit: 30
};
var quizConfig2Dan = {
    questionCount: 50,
    optionCount: 3,
    levelMin: 1,
    levelMax: 12,
    categoryId: 0,
    timeLimit: 30
};
var quizConfig3Dan = {
    questionCount: 50,
    optionCount: 3,
    levelMin: 1,
    levelMax: 13,
    categoryId: 0,
    timeLimit: 30
};
var quizConfig4Dan = {
    questionCount: 50,
    optionCount: 3,
    levelMin: 1,
    levelMax: 14,
    categoryId: 0,
    timeLimit: 30
};
var quizConfig5Dan = {
    questionCount: 50,
    optionCount: 3,
    levelMin: 1,
    levelMax: 15,
    categoryId: 0,
    timeLimit: 30
};
var quizConfig6Dan = {
    questionCount: 50,
    optionCount: 3,
    levelMin: 1,
    levelMax: 16,
    categoryId: 0,
    timeLimit: 30
};
var _a;
var routeNames = {
    index: '/',
    signIn: '/log-ind',
    frontPage: '/forside',
    createUser: '/opret-bruger',
    quizCategory: '/quiz-category',
    quizConfig: '/quiz-configuration',
    quiz: '/quiz',
    curriculum: '/pensum',
    result: '/resultat'
};
var routes = (_a = {},
    _a[routeNames.index] = pageIndex,
    _a[routeNames.signIn] = pageIndex,
    _a[routeNames.frontPage] = pageIndex,
    _a[routeNames.createUser] = pageCreateUser,
    _a[routeNames.curriculum] = pageIndex,
    _a[routeNames.quizCategory] = pageQuizCategory,
    _a[routeNames.quizConfig] = pageQuizConfig,
    _a[routeNames.quiz] = pageQuiz,
    _a[routeNames.result] = pageQuizResult,
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
function templateQuiz(context) {
    setTemplate("handlebars-quiz", "article", context);
}
function templateQuizResult(context) {
    setTemplate("handlebars-quiz-result", "article", context);
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
                            errorLevel: infoBoxErrorLevel.error,
                            title: "Valideringsfejl",
                            message: "Du skal indtaste en email",
                            buttonAction: 'pageCreateUser()',
                            buttonText: 'Create User'
                        });
                        return [2];
                    }
                    if (password.value !== passwordRepeat.value) {
                        pageInfo({
                            errorLevel: infoBoxErrorLevel.error,
                            title: "Valideringsfejl",
                            message: "Passwords skal være forskelige",
                            buttonAction: 'pageCreateUser()',
                            buttonText: 'Create User'
                        });
                        return [2];
                    }
                    if (!password.value || !passwordRepeat.value) {
                        pageInfo({
                            errorLevel: infoBoxErrorLevel.error,
                            title: "Valideringsfejl",
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
                        message = "<p>Vi har nu oprettet din nye profil. Nu mangler du blot at aktivere den" +
                            " via det link jeg netop har send til dig :)</p><br><p>Med venlig hilsen,</p><p>Grand Master Kwon!</p>";
                        pageInfo({
                            errorLevel: infoBoxErrorLevel.success,
                            title: "Tillykke",
                            message: message,
                            buttonText: 'Log ind',
                            buttonAction: 'pageIndex()'
                        });
                        return [2, true];
                    }
                    pageInfo({
                        errorLevel: infoBoxErrorLevel.error,
                        title: "Valideringsfejl",
                        message: "Emailen er allerede optaget. Måske har du glemt dit password?",
                        buttonAction: 'pageCreateUser()',
                        buttonText: 'Prøv igen'
                    });
                    return [2, false];
            }
        });
    });
}
//# sourceMappingURL=build.js.map