// import Handlebars from 'handlebars';

type Template =
    'handlebars-sign-in-form'
    | 'handlebars-main-menu'
    | 'handlebars-top-bar-signed-in'
    | 'handlebars-top-bar-signed-out'
    | 'handlebars-create-user'
    | 'handlebars-info'
    | 'handlebars-loading'
    | 'handlebars-quiz-category'
    | 'handlebars-quiz-configuration'
    | 'handlebars-quiz'
    | 'handlebars-quiz-result'
    | 'handlebars-quiz-wrong-answer'
    | 'handlebars-curriculum';


type ContentTarget = 'header' | 'article' | 'footer';

function setTemplate(templateId: Template, contentTarget: ContentTarget, context: Object = {}) {
    let template = document.getElementById(templateId).innerHTML;
    // @ts-ignore
    let templateScript = Handlebars.compile(template);
    let html = templateScript(context);
    let contentContainer: HTMLElement = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}

function templateQuizCategory(): void {
    setTemplate("handlebars-quiz-category", "article")
}

function templateQuizConfig(config: QuizConfigurationOptions): void {
    let select = [];

    Object.keys(config).forEach((k: string, i: number) => {
            if (k !== 'displayNames') {
                select.push(`<div class="select-row"><label>${config['displayNames'][k]}</label><select id="select-${i}">${config[k].map((o: string) => `<option>${o}</option>`).join('')}</select></div>`)
            }
        }
    );

    setTemplate("handlebars-quiz-configuration", "article", {select: `<form id='quiz-config-form'>${select.join('')}</form>`})
}

function templateCurriculum(context: {select: string, rows: string}): void {
    setTemplate("handlebars-curriculum", "article", context)
}

function templateQuiz(context: {percentageComplete: number, progressBarText: string, category: string, question: string, options: string}): void {
    setTemplate("handlebars-quiz", "article", context)
}

function templateQuizResult(context: {stars: string, percentageCorrect: number, category: string, timeSpent: string, answers: string}): void {
    setTemplate("handlebars-quiz-result", "article", context)
}

function templateMainMenu(): void {
    setTemplate("handlebars-main-menu", "article")
}

function templateSignIn(context?: { message: string, extra: string }): void {
    setTemplate('handlebars-sign-in-form', "article", context);
}

function templateCreateUser(): void {
    setTemplate('handlebars-create-user', "article");
}

type ComponentInfo = {
    errorLevel: string;
    title: string;
    message: string;
    buttonAction: string;
    buttonText: string;
}

function templateInfo(context: ComponentInfo): void {
    setTemplate('handlebars-info', "article", context);
}

function templateTopBarSignedIn(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-in", "header", context)
}

function templateTopBarSignedOut(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-out", "header", context)
}

function templateLoading(): void {
    setTemplate('handlebars-loading', 'article')
}


