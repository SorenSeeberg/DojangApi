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

type Answer = {
    text: string;
    correct: boolean;
}

type Result = {
    categoryName: string;
    quizToken: string;
    percentageCorrect: number;
    timeSpent: number;
    answers: Answer[];
}

async function handleCreateNewQuizFromForm(){
        const select0 = <HTMLSelectElement>document.getElementById('select-0');
        const select1 = <HTMLSelectElement>document.getElementById('select-1');
        const select2 = <HTMLSelectElement>document.getElementById('select-2');
        const select3 = <HTMLSelectElement>document.getElementById('select-3');
        const select4 = <HTMLSelectElement>document.getElementById('select-4');
        const select5 = <HTMLSelectElement>document.getElementById('select-5');

        const categoryId: number = select0.selectedIndex;
        const levelMin: number = select1.selectedIndex;
        const levelMax: number = select2.selectedIndex;
        const questionCount: number = parseInt(select3.value);
        const optionCount: number= parseInt(select4.value);
        const timeLimit: number = parseInt(select5.value);

        const config: QuizConfiguration = { categoryId, levelMin, levelMax, questionCount, optionCount, timeLimit };
        console.log('CONFIG');
        console.log(config);

        await handleCreateNewQuiz(config);
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
        clearQuizToken();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleCreateNewQuiz(quizConfig: QuizConfiguration) {
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
        clearQuizToken();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleGetResult() {
    const quizToken = getQuizToken();

    let response = await fetch(`/quiz/result/${quizToken}`, {
        method: "get",
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        const result: Result = responseObject.body;
        pageQuizResult(result);
        return true;
    }
    if (responseObject.status === 401) {
        pageInfo401();
        clearQuizToken();
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
        if (!responseObject.body.complete) {
            pageQuiz(quiz);
        } else {
            console.log('Complete!');
            pageLoading();
            await handleGetResult();
        }
        return true;
    }
    if (responseObject.status === 401) {
        pageInfo401();
        clearQuizToken();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleClearQuiz() {

}

async function handleAnswerQuestion(optionIndex: number) {
    const quizToken = getQuizToken();
    let response = await fetch(`/quiz/question/${quizToken}`, {
        method: 'put',
        body: JSON.stringify({optionIndex}),
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        console.log(responseObject);

        if (responseObject.body.answer === true) {
            console.log('Korrekt');
            await handleGetQuiz();

        } else {
            console.log('Forkert');
            pageInfo({
                title: 'Svaret er forkert',
                message: responseObject.body.text,
                errorLevel: infoBoxErrorLevel.error,
                buttonText: 'Næste spørgsmål',
                buttonAction: 'handleGetQuiz()'
            })
        }
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        clearQuizToken();
        return false;
    }

    pageInfo404();
    return false;

}