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
var DEV = true;
var ORIGIN = DEV ? 'http://127.0.0.1:5000' : 'http://sorenseeberg.pythonanywhere.com';
function handleUpdateCurriculumFromForm() {
    return __awaiter(this, void 0, void 0, function () {
        var select0, select1, select2, categoryId, levelMin, levelMax;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    select0 = document.getElementById('select-curriculum-category');
                    select1 = document.getElementById('select-curriculum-level-min');
                    select2 = document.getElementById('select-curriculum-level-max');
                    categoryId = select0.selectedIndex;
                    levelMin = select1.selectedIndex + 1;
                    levelMax = select2.selectedIndex + 1;
                    return [4, handleGetCurriculum(categoryId, levelMin, levelMax)];
                case 1:
                    _a.sent();
                    return [2];
            }
        });
    });
}
function handleGetCurriculum(categoryId, levelMin, levelMax) {
    return __awaiter(this, void 0, void 0, function () {
        var response, responseObject, curriculum;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    templateLoading();
                    return [4, fetch("/curriculum?categoryId=" + categoryId + "&levelMin=" + levelMin + "&levelMax=" + levelMax, {
                            method: 'get',
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        if (DEV) {
                            console.log(responseObject);
                        }
                        curriculum = responseObject.body;
                        pageCurriculum(curriculum);
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        pageInfo401();
                        clearQuizToken();
                        clearAccessToken();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
var TITLE_CONTEXT = { title: 'Dojang' };
function starBuilder(percentage) {
    var star = '&#10026;';
    return percentage === 100
        ? "<h1 class=\"gold-font star\">" + star + " " + star + " " + star + "</h1><p>Perfekt</p>"
        : percentage >= 90
            ? "<h1 class=\"silver-font star\">" + star + " " + star + "</h1><p>Flot pr\u00E6station</p>"
            : percentage >= 75
                ? "<h1 class=\"bronze-font star\">" + star + "</h1><p>Du klarede den lige</p>"
                : '<h3 class="runner-up-font">Ikke bestået</h3><p>Wax on  . . was off . .</p>';
}
function starsRowBuilder(percentage) {
    var star = '&#10026;';
    return percentage === 100
        ? "<p class=\"gold-font star\">" + star + " " + star + " " + star + "</p>"
        : percentage >= 90
            ? "<p class=\"silver-font star\">" + star + " " + star + "</p>"
            : percentage >= 75
                ? "<p class=\"bronze-font star\">" + star + "</p>"
                : '<p></p>';
}
function pageIndex() {
    if (!getAccessToken()) {
        historyRouter({ data: null, path: routeNames.signIn });
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateSignIn();
    }
    else {
        historyRouter({ data: null, path: routeNames.frontPage });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateMainMenu();
    }
}
function pageCreateUser() {
    if (!getAccessToken()) {
        historyRouter({ data: null, path: routeNames.createUser });
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
    historyRouter({ data: null, path: '' });
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
function pageCurrentUser(user) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        var resultRows = "" + user.results.map(function (r) { return "<tr><td>" + r.level + "</td><td>" + r.timeSpent + "</td><td>" + starsRowBuilder(r.percentageCorrect) + "</td></tr>"; }).join('');
        var context = { email: user.email, resultRows: resultRows };
        historyRouter({ data: null, path: routeNames.currentUser });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateCurrentUser(context);
    }
}
function pageQuizCategory() {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, path: routeNames.quizCategory });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizCategory();
    }
}
function pageQuizConfig(config) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, path: routeNames.quizConfig });
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
        historyRouter({ data: quiz.quizToken, path: routeNames.quiz });
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuiz(context);
    }
}
function pageQuizResult(result) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, path: routeNames.result + "/" + result.quizToken });
        var stars = starBuilder(result.percentageCorrect);
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
function pageCurriculum(curriculum) {
    if (!getAccessToken()) {
        pageIndex();
    }
    else {
        historyRouter({ data: null, path: "" + routeNames.curriculum });
        var selectCategory = "<div class=\"select-row\"><label>Kategori</label><select id=\"select-curriculum-category\">" + curriculum.categoryLabels.map(function (c) { return c === curriculum.categoryLabel ? "<option selected>" + c + "</option>" : "<option>" + c + "</option>"; }).join('') + "</select></div>";
        var selectLevelMin = "<div class=\"select-row\"><label>Laveste grad</label><select id=\"select-curriculum-level-min\">" + curriculum.levelLabels.map(function (l) { return l === curriculum.levelMinLabel ? "<option selected>" + l + "</option>" : "<option>" + l + "</option>"; }).join('') + "</select></div>";
        var selectLevelMan = "<div class=\"select-row\"><label>H\u00F8jeste grad</label><select id=\"select-curriculum-level-max\">" + curriculum.levelLabels.map(function (l) { return l === curriculum.levelMaxLabel ? "<option selected>" + l + "</option>" : "<option>" + l + "</option>"; }).join('') + "</select></div>";
        var rows = "" + curriculum.data.map(function (row) { return "<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td></tr>"; }).join('');
        var context = { rows: rows, select: selectCategory + selectLevelMin + selectLevelMan };
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateCurriculum(context);
    }
}
function handleCreateNewQuizFromForm() {
    return __awaiter(this, void 0, void 0, function () {
        var select0, select1, select2, select3, select4, select5, categoryId, levelMin, levelMax, questionCount, optionCount, timeLimit, config;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    select0 = document.getElementById('select-0');
                    select1 = document.getElementById('select-1');
                    select2 = document.getElementById('select-2');
                    select3 = document.getElementById('select-3');
                    select4 = document.getElementById('select-4');
                    select5 = document.getElementById('select-5');
                    categoryId = select0.selectedIndex;
                    levelMin = select1.selectedIndex;
                    levelMax = select2.selectedIndex;
                    questionCount = parseInt(select3.value);
                    optionCount = parseInt(select4.value);
                    timeLimit = parseInt(select5.value);
                    config = { categoryId: categoryId, levelMin: levelMin, levelMax: levelMax, questionCount: questionCount, optionCount: optionCount, timeLimit: timeLimit };
                    return [4, handleCreateNewQuiz(config)];
                case 1:
                    _a.sent();
                    return [2];
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
                        clearQuizToken();
                        clearAccessToken();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
function handleCreateNewQuiz(quizConfig) {
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
                        setQuizToken(quiz.quizToken);
                        pageQuiz(quiz);
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        pageInfo401();
                        clearQuizToken();
                        clearAccessToken();
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
                    templateLoading();
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
                        clearQuizToken();
                        clearAccessToken();
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
                    templateLoading();
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
                    pageLoading();
                    return [4, handleGetResult()];
                case 4:
                    _a.sent();
                    _a.label = 5;
                case 5: return [2, true];
                case 6:
                    if (responseObject.status === 401) {
                        pageInfo401();
                        clearQuizToken();
                        clearAccessToken();
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
                    templateLoading();
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
                    if (!(responseObject.body.answer === true)) return [3, 4];
                    return [4, handleGetQuiz()];
                case 3:
                    _a.sent();
                    return [3, 5];
                case 4:
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
                        clearQuizToken();
                        clearAccessToken();
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
    currentUser: '/min-bruger',
    quiz: '/quiz',
    curriculum: '/pensum',
    result: '/resultat',
};
var routes = (_a = {},
    _a[routeNames.index] = pageIndex,
    _a[routeNames.signIn] = pageIndex,
    _a[routeNames.frontPage] = pageIndex,
    _a[routeNames.createUser] = pageCreateUser,
    _a[routeNames.curriculum] = function () { return handleGetCurriculum(1, 1, 11); },
    _a[routeNames.quizCategory] = pageQuizCategory,
    _a[routeNames.quizConfig] = pageQuizConfig,
    _a[routeNames.quiz] = pageQuiz,
    _a[routeNames.result] = pageQuizResult,
    _a[routeNames.currentUser] = handleGetCurrentUser,
    _a);
function spaRouter() {
    if (DEV) {
        console.log('spaRouter');
        console.log(window.location.pathname);
        console.log(routes);
    }
    routes[window.location.pathname]();
}
function historyRouter(url, type) {
    if (type === void 0) { type = 'push'; }
    if (DEV) {
        console.log('historyRouter');
        console.log(url);
    }
    type === 'push'
        ? history.pushState(url.data, url.path, ORIGIN + url.path)
        : history.replaceState(url.data, url.path, ORIGIN + url.path);
}
function setTemplate(templateId, contentTarget, context) {
    if (context === void 0) { context = {}; }
    var template = document.getElementById(templateId).innerHTML;
    var templateScript = Handlebars.compile(template);
    var html = templateScript(context);
    var contentContainer = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}
function templateCurrentUser(context) {
    setTemplate("handlebars-current-user", "article", context);
}
function templateQuizCategory() {
    setTemplate("handlebars-quiz-category", "article");
}
function templateQuizConfig(config) {
    var select = [];
    Object.keys(config).forEach(function (k, i) {
        if (k !== 'displayNames') {
            select.push("<div class=\"select-row\"><label>" + config['displayNames'][k] + "</label><select id=\"select-" + i + "\">" + config[k].map(function (o) { return "<option>" + o + "</option>"; }).join('') + "</select></div>");
        }
    });
    setTemplate("handlebars-quiz-configuration", "article", { select: "<form id='quiz-config-form'>" + select.join('') + "</form>" });
}
function templateCurriculum(context) {
    setTemplate("handlebars-curriculum", "article", context);
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
function handleSignOut() {
    return __awaiter(this, void 0, void 0, function () {
        var response, responseObject;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    templateLoading();
                    return [4, fetch("/users/sign-out", {
                            method: "get",
                            headers: getAuthorizationHeader()
                        })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        clearAccessToken();
                        clearQuizToken();
                        pageIndex();
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        clearQuizToken();
                        clearAccessToken();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
var Handler = (function () {
    function Handler() {
    }
    return Handler;
}());
function handleCreateUser() {
    return __awaiter(this, void 0, void 0, function () {
        var email, password, passwordRepeat, formData, response, responseObject, message;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    email = document.getElementById('input-field-email');
                    password = document.getElementById('input-field-password');
                    passwordRepeat = document.getElementById('input-field-password-repeat');
                    pageLoading(false);
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
                        message = "<p>Jeg har nu oprettet din nye profil, men den er endnu ikke aktiv. Du kan aktivere den" +
                            " ved at trykke på det link jeg netop har sendt til dig på mail :)</p><br><p>Med venlig hilsen,</p>" +
                            "<p>Grand Master Kwon</p>";
                        pageInfo({
                            errorLevel: infoBoxErrorLevel.success,
                            title: "Hov Vent!",
                            message: message,
                            buttonText: 'Log ind',
                            buttonAction: 'pageIndex()'
                        });
                        return [2, true];
                    }
                    pageInfo({
                        errorLevel: infoBoxErrorLevel.error,
                        title: "Fejl!",
                        message: "Emailen er allerede optaget. Måske har du glemt dit password?",
                        buttonAction: 'pageCreateUser()',
                        buttonText: 'Prøv igen'
                    });
                    return [2, false];
            }
        });
    });
}
function handleGetCurrentUser() {
    return __awaiter(this, void 0, void 0, function () {
        var response, responseObject, user;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4, fetch("/users/current-user", {
                        method: "get",
                        headers: getAuthorizationHeader()
                    })];
                case 1:
                    response = _a.sent();
                    return [4, response.json()];
                case 2:
                    responseObject = _a.sent();
                    if (responseObject.status === 200) {
                        user = responseObject.body;
                        pageCurrentUser(user);
                        return [2, true];
                    }
                    if (responseObject.status === 401) {
                        pageInfo401();
                        clearQuizToken();
                        clearAccessToken();
                        return [2, false];
                    }
                    pageInfo404();
                    return [2, false];
            }
        });
    });
}
//# sourceMappingURL=build.js.map