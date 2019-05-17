type QuizConfigurationOptions = {
    categories: string[];
    levelsMin: string[];
    levelsMax: string[];
    questionCount: number[];
    optionCount: number[];
    timeLimit: number[];
    displayNames: {}
}

type QuizConfiguration = {
    categoryId: number;
    levelMin: number;
    levelMax: number;
    questionCount: number;
    optionCount: number;
    timeLimit: number;
}

type Quiz = {
    currentQuestion: number;
    levelMax: number;
    levelMin: number;
    optionCount: number;
    quizToken: string;
    title: string;
    totalQuestions: number;
}

async function handleGetQuizConfiguration() {

    templateLoading();

    let response = await fetch('/quiz/configuration', {
        method: "get",
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        templateTopBarSignedIn(TITLE_CONTEXT);
        templateQuizConfig(responseObject.body);
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleCreateNewQuiz() {
    const quiz: QuizConfiguration = {
        categoryId: 2,
        levelMin: 3,
        levelMax: 8,
        questionCount: 25,
        optionCount: 3,
        timeLimit: 10
    };

    templateLoading();

    let response = await fetch('/quiz', {
        method: "post",
        body: JSON.stringify(quiz),
        headers: getAuthorizationHeader()
    });
    let responseObject = await response.json();

    if (responseObject.status === 201) {
        const quiz: Quiz = responseObject.body;
        setQuizToken(quiz.quizToken);
        pageInfo({message: 'Yep', buttonAction: 'pageIndex()', buttonText: 'Hell Yes!'});
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }
    pageInfo404();
    return false;

}