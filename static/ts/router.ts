const routeNames = {
    index: '/',
    signIn: '/log-ind',
    frontPage: '/forside',
    createUser: '/opret-bruger',
    quizCategory: '/quiz-category',
    quizConfig: '/quiz-configuration',
    quiz: '/quiz',
    curriculum: '/pensum'
};

const routes: { [key: string]: () => void } = {
    [routeNames.index]: pageIndex,
    [routeNames.signIn]: pageIndex,
    [routeNames.frontPage]: pageIndex,
    [routeNames.createUser]: pageCreateUser,
    [routeNames.curriculum]: pageIndex,
    [routeNames.quizCategory]: pageQuizCategory,
    [routeNames.quizConfig]: pageQuizConfig,
    [routeNames.quiz]: pageQuiz
};

function spaRouter(): void {
    console.log('spaRouter');
    console.log(window.location.pathname);
    console.log(routes);
    routes[window.location.pathname]();
}

type Url = {
    data: any;
    title: string;
    url: string;
}

function historyRouter(url: Url): void {
    console.log('historyRouter');
    console.log(url);
    console.log(routes);

    history.pushState(url.data, url.title, url.url);
    // history.replaceState(url.data, url.title, url.url);
}