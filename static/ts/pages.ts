const TITLE_CONTEXT = {title: 'Dojang'};

function pageIndex(): void {
    if (!getAccessToken()) {
        historyRouter({data: null, title: '', url: routeNames.signIn});
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateSignIn();
    } else {
        historyRouter({data: null, title: '', url: routeNames.frontPage});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateMainMenu();
    }
}

function pageCreateUser(): void {
    if (!getAccessToken()) {
        historyRouter({data: null, title: '', url: routeNames.createUser});
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateCreateUser();
    } else {
        pageIndex();
    }
}

const infoBoxErrorLevel = {
    info: 'info-box',
    error: 'info-box error',
    success: 'info-box success'
};

function pageInfo(context: ComponentInfo): void {
    historyRouter({data: null, title: '', url: ''});
    templateTopBarSignedOut(TITLE_CONTEXT);
    templateInfo(context);
}

function pageInfo401(): void {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "401 Unauthorized",
        message: "",
        buttonAction: "pageIndex()",
        buttonText: "Til forsiden"
    });
}

function pageInfo404(): void {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "404 Not Found",
        message: "",
        buttonAction: "pageIndex()",
        buttonText: "Til forsiden"
    });
}

function pageLoading(loggedIn: boolean = true): void {
    loggedIn
        ? templateTopBarSignedIn(TITLE_CONTEXT)
        : templateTopBarSignedOut(TITLE_CONTEXT);

    templateLoading()
}

function pageQuizCategory(): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, title: '', url: routeNames.quizCategory});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizCategory();
    }
}

function pageQuizConfig(config: QuizConfigurationOptions): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, title: '', url: routeNames.quizConfig});
        handleGetQuizConfiguration();
    }
}

function pageQuiz(quiz: Quiz): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        const options: string = quiz.currentQuestion.options.map((o: Option) => `<button class="btn btn-large-wide btn-secondary" type="button" onclick="handleAnswerQuestion(${o.index})">${o.option}</button>`).join('');
        const context = {
            percentageComplete: Math.round(quiz.currentQuestionIndex / quiz.totalQuestions * 100),
            progressBarText: `${quiz.currentQuestionIndex} / ${quiz.totalQuestions}`,
            category: quiz.title,
            question: quiz.currentQuestion.question,
            options
        };
        historyRouter({data: quiz.quizToken, title: '', url: routeNames.quiz});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuiz(context);
    }
}

function pageQuizResult(quiz: Quiz): void {
     if (!getAccessToken()) {
        pageIndex();
    } else {
         const context = {category: quiz.title, percentageCorrect: 80, timeSpent: '1:43', answers: ''};
         templateTopBarSignedIn(TITLE_CONTEXT);
         templateQuizResult(context)
     }
}