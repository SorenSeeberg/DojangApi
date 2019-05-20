const TITLE_CONTEXT = {title: 'Dojang'};

function pageIndex(): void {
    if (!getAccessToken()) {
        historyRouter({data: null, path: routeNames.signIn});
        templateTopBarSignedOut(TITLE_CONTEXT);
        templateSignIn();
    } else {
        historyRouter({data: null, path: routeNames.frontPage});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateMainMenu();
    }
}

function pageCreateUser(): void {
    if (!getAccessToken()) {
        historyRouter({data: null, path: routeNames.createUser});
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
    historyRouter({data: null, path: ''});
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

function pageInfoNotImplemented(): void {
    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "Not Implemented",
        message: "På vej",
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
        historyRouter({data: null, path: routeNames.quizCategory});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizCategory();
    }
}

function pageQuizConfig(config: QuizConfigurationOptions): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, path: routeNames.quizConfig});
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
        historyRouter({data: quiz.quizToken, path: routeNames.quiz});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuiz(context);
    }
}

function pageQuizResult(result: Result): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, path: `${routeNames.result}/${result.quizToken}`});
        const star = '&#10026;';

        const stars = result.percentageCorrect === 100
            ? `<h1 class="gold-font star">${star} ${star} ${star}</h1><p>Perfekt</p>`
            : result.percentageCorrect >= 90
                ? `<h1 class="silver-font star">${star} ${star}</h1><p>Flot præstation</p>`
                : result.percentageCorrect >= 75
                    ? `<h1 class="bronze-font star">${star}</h1><p>Du klarede den lige</p>`
                    : '<h3 class="runner-up-font">Ikke bestået</h3><p>Wax on  . . was off . .</p>';

        const minutes: number = Math.floor(result.timeSpent / 60);
        const seconds: number = Math.floor(result.timeSpent - (minutes * 60));

        const timeSpent = `${minutes}:${seconds > 9 ? seconds : `0${seconds}`}`;
        const context = {
            category: `${result.categoryName}`,
            stars,
            percentageCorrect: result.percentageCorrect,
            timeSpent,
            answers: result.answers.map((a: Answer, i: number) => `<p class="${a.correct ? '' : 'error'}">${i + 1}. ${a.text}</p>`).join('')
        };

        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizResult(context)
    }
}

function pageCurriculum(curriculum: Curriculum): void {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: {test: 3}, path: `${routeNames.curriculum}`});

        const selectCategory = `<div class="select-row"><label>Kategori</label><select>${curriculum.categoryLabels.map(c => c === curriculum.categoryLabel ? `<option selected>${c}</option>` : `<option>${c}</option>`).join('')}</select></div>`;
        const selectLevelMin = `<div class="select-row"><label>Laveste grad</label><select>${curriculum.levelLabels.map(l => l === curriculum.levelMinLabel ? `<option selected>${l}</option>` : `<option>${l}</option>`).join('')}</select></div>`;
        const selectLevelMan = `<div class="select-row"><label>Højeste grad</label><select>${curriculum.levelLabels.map(l => l === curriculum.levelMaxLabel ? `<option selected>${l}</option>` : `<option>${l}</option>`).join('')}</select></div>`;
        const rows = `<form>${curriculum.data.map(row => `<tr><td>${row[0]}</td><td>${row[1]}</td><td>${row[2]}</td></tr>`).join('')}</form>`;
        const context = {rows, select: selectCategory + selectLevelMin + selectLevelMan};

        templateTopBarSignedIn(TITLE_CONTEXT);
        templateCurriculum(context);
    }
}
