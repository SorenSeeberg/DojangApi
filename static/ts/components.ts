type Template =
    'handlebars-sign-in-form'
    | 'handlebars-main-menu'
    | 'handlebars-top-bar-signed-in'
    | 'handlebars-top-bar-signed-out';
type ContentTarget = 'header' | 'article' | 'footer';

function setTemplate(templateId: Template, contentTarget: ContentTarget, context: Object = {}) {
    let template = document.getElementById(templateId).innerHTML;
    // @ts-ignore
    let templateScript = Handlebars.compile(template);
    let html = templateScript(context);
    let contentContainer: HTMLElement = document.getElementById(contentTarget);
    contentContainer.innerHTML = html;
}

async function handleSignIn() {
    const email = <HTMLInputElement>document.getElementById('input-field-email');
    const password = <HTMLInputElement>document.getElementById('input-field-password');

    let formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);

    let response = await fetch('/users/sign-in', {
        body: formData,
        method: "post"
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        setAccessToken(responseObject.body.accessToken);
        pageIndex();
        return true;
    }
    return false;
}

function componentMainMenu(): void {
    setTemplate("handlebars-main-menu", "article")
}

function componentSignIn(): void {
    setTemplate('handlebars-sign-in-form', "article");
}

function componentTopBarSignedIn(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-in", "header", context)
}

function componentTopBarSignedOut(context: { title: string }): void {
    setTemplate("handlebars-top-bar-signed-out", "header", context)
}



