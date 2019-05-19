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

type Option = { index: number; option: string }

type Question = {
    index: number;
    question: string;
    options: Option[]
}

type Quiz = {
    levelMax: number;
    levelMin: number;
    optionCount: number;
    quizToken: string;
    title: string;
    totalQuestions: number;
    currentQuestionIndex: number;
    currentQuestion: Question;
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

async function handleCreateNewQuiz(quizConfig: QuizConfiguration = quizConfigTemp) {
    templateLoading();

    let response = await fetch('/quiz', {
        method: "post",
        body: JSON.stringify(quizConfig),
        headers: getAuthorizationHeader()
    });
    let responseObject = await response.json();

    if (responseObject.status === 201) {
        const quiz: Quiz = responseObject.body;
        console.log(quiz);
        setQuizToken(quiz.quizToken);
        pageQuiz(quiz);
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleGetQuiz() {
    const quizToken = getQuizToken();

    let response = await fetch(`/quiz/${quizToken}`, {
        method: "get",
        headers: getAuthorizationHeader()
    });
    let responseObject = await response.json();

    if (responseObject.status === 200) {
        const quiz: Quiz = responseObject.body;
        pageQuiz(quiz);
        return true;
    }
    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleAnswerQuestion(optionIndex: number) {
    const quizToken = getQuizToken();
    let response = await fetch(`/quiz/question/${quizToken}`, {
        method:'put',
        body:JSON.stringify({optionIndex}),
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        console.log(responseObject);

        if (responseObject.answer) {
            console.log('Korrekt');
            await handleGetQuiz();

        }
        else {
            console.log('Forkert');
            await handleGetQuiz();
        }
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }

    pageInfo404();
    return false;

}