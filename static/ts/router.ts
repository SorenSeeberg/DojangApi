const routeNames = {
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

const routes: { [key: string]: any } = {
    [routeNames.index]: pageIndex,
    [routeNames.signIn]: pageIndex,
    [routeNames.frontPage]: pageIndex,
    [routeNames.createUser]: pageCreateUser,
    [routeNames.curriculum]: () => handleGetCurriculum(1,1,11),
    [routeNames.quizCategory]: pageQuizCategory,
    [routeNames.quizConfig]: pageQuizConfig,
    [routeNames.quiz]: pageQuiz,
    [routeNames.result]: pageQuizResult,
    [routeNames.currentUser]: handleGetCurrentUser
};

function spaRouter(): void {
    if (DEV) {
        console.log('spaRouter');
        console.log(window.location.pathname);
        console.log(routes);
    }
    routes[window.location.pathname]();
}

type Url = {
    data: any;
    path: string;
}

function historyRouter(url: Url, type: 'push' |'replace' = 'push'): void {
    if (DEV) {
        console.log('historyRouter');
        console.log(url);
    }

    type === 'push'
        ? history.pushState(url.data, url.path, ORIGIN + url.path)
        : history.replaceState(url.data, url.path, ORIGIN + url.path);
}