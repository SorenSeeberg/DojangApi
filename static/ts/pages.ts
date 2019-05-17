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

function pageInfo(context: ComponentInfo): void {
    historyRouter({data: null, title: '', url: ''});
    templateTopBarSignedOut(TITLE_CONTEXT);
    templateInfo(context);
}

function pageInfo401(): void {
    pageInfo({message: "<h1>401 Unauthorized</h1>", buttonAction: "pageIndex()", buttonText: "Til forsiden" });
}

function pageInfo404(): void {
    pageInfo({message: "<h1>404 Not Found</h1>", buttonAction: "pageIndex()", buttonText: "Til forsiden" });
}

function pageLoading(loggedIn: boolean = true) {
    loggedIn
        ? templateTopBarSignedIn(TITLE_CONTEXT)
        : templateTopBarSignedOut(TITLE_CONTEXT);

    templateLoading()
}

function pageQuizCategory() {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, title: '', url: routeNames.quizCategory});
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizCategory();
    }
}

function pageQuizConfig(config: QuizConfigurationOptions) {
    if (!getAccessToken()) {
        pageIndex();
    } else {
        historyRouter({data: null, title: '', url: routeNames.quizConfig});
        handleGetQuizConfiguration();

    }
}