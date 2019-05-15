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

function handleSignIn(): void {
    console.log("Sign in !");

    // @ts-ignore
    const email: string = document.getElementById('input-field-email').value;
    // @ts-ignore
    const password: string = document.getElementById('input-field-password').value;

    let formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    fetch("/users/sign-in",
        {
            body: formData,
            method: "post"
        }).then((response) => {
        if (response.status === 200) {
            console.log('Du er nu logget ind');
        } else if (response.status === 401) {
            console.log('Email og/eller password er forkert!');
        }
        return response.json()
    }).then((responseObject) => {
        if (responseObject.status === 200) {
            setAccessToken(responseObject.body.accessToken);
            pageIndex();
        }
        console.log(responseObject);
    });
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



