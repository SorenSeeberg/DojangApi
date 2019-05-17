// import Handlebars from 'handlebars';

type Template =
    'handlebars-sign-in-form'
    | 'handlebars-main-menu'
    | 'handlebars-top-bar-signed-in'
    | 'handlebars-top-bar-signed-out'
    | 'handlebars-sign-in-form-error'
    | 'handlebars-create-user'
    | 'handlebars-created-user'
    | 'handlebars-loading';


type ContentTarget = 'header' | 'article' | 'footer';

function setTemplate(templateId: Template, contentTarget: ContentTarget, context: Object = {}) {
    let template = document.getElementById(templateId).innerHTML;
    let templateScript = Handlebars.compile(template);
    let html = templateScript(context);
    let contentContainer: HTMLElement = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}


function componentMainMenu(): void {
    setTemplate("handlebars-main-menu", "article")
}

function componentSignIn(): void {
    setTemplate('handlebars-sign-in-form', "article");
}

function templateSignInError(): void {
    setTemplate('handlebars-sign-in-form-error', "article");
}

function componentCreateUser(): void {
    setTemplate('handlebars-create-user', "article");
}

function componentCreatedUser(): void {
    setTemplate('handlebars-created-user', "article");
}

function componentTopBarSignedIn(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-in", "header", context)
}

function componentTopBarSignedOut(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-out", "header", context)
}

function templateLoading(): void {
    setTemplate('handlebars-loading', 'article')
}


