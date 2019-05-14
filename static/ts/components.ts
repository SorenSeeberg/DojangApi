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
        if (response.status == 200) {
            console.log('Du er nu logget ind');
        } else if (response.status == 401) {
            console.log('Email og/eller password er forkert!');
        }
        return response.json()
    }).then((myJson) => {
        console.log(myJson);
    });
}

function signIn(): void {

    let template = document.getElementById('handlebars-sign-in-form').innerHTML;
    // Compile the template data into a function
    // @ts-ignore
    let templateScript = Handlebars.compile(template);
    let context = {"name": "Ritesh Kumar", "occupation": "developer"};
    let html = templateScript(context);
    let articleElement: HTMLElement = document.getElementById('article');
    articleElement.innerHTML = html;
}

function componentHeader(loggedIn: boolean = true): void {
    let title = "Dojang";
    let headerElement: HTMLElement = document.getElementById('header');

    if (loggedIn) {
        headerElement.innerHTML = `<div>${title}</div><div class='header-profile'/>`;
    } else {
        headerElement.innerHTML = `<div>${title}</div>`;
    }

    signIn();
}

function componentSignIn() {

    let articleElement: HTMLElement = document.getElementById('article');

}