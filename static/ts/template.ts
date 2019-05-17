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
    | 'handlebars-quiz-configuration';


type ContentTarget = 'header' | 'article' | 'footer';

function setTemplate(templateId: Template, contentTarget: ContentTarget, context: Object = {}) {
    let template = document.getElementById(templateId).innerHTML;
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

    console.log('templateQuizConfig');
    console.log(config);

    Object.keys(config).forEach(k =>{
        if (k !== 'displayNames') {
            select.push(`<label>${config['displayNames'][k]}</label><select>${config[k].map(o => `<option>${o}</option>`).join('')}</select>`)
        }
    }
    );

    setTemplate("handlebars-quiz-configuration", "article", {select: select.join('')})
}

function templateMainMenu(): void {
    setTemplate("handlebars-main-menu", "article")
}

function templateSignIn(context?:{message:string, extra:string}): void {
    setTemplate('handlebars-sign-in-form', "article", context);
}

function templateCreateUser(): void {
    setTemplate('handlebars-create-user', "article");
}

type ComponentInfo = {
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


