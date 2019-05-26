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
    console.log('spaRouter');
    console.log(window.location.pathname);
    console.log(routes);
    routes[window.location.pathname]();
}

type Url = {
    data: any;
    path: string;
}

function historyRouter(url: Url, type: 'push' |'replace' = 'push'): void {
    console.log('historyRouter');
    console.log(url);
    // const origin = 'http://127.0.0.1:5000';
    const origin = 'http://sorenseeberg.pythonanywhere.com';

    console.log(origin + url.path);

    type === 'push'
        ? history.pushState(url.data, url.path, origin + url.path)
        : history.replaceState(url.data, url.path, origin + url.path);

    console.log(history.length)
}