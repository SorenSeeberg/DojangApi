async function handleSignIn() {

    const email = <HTMLInputElement>document.getElementById('input-field-email');
    const password = <HTMLInputElement>document.getElementById('input-field-password');

    templateLoading();

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
    templateSignIn({
        message: '<p class="clr-error">Email og/eller password er ikke korrekt</p>',
        extra: '<button class="btn btn-link" type="button" onclick="pageCreateUser()">Glemt password?</button>'
    });
    return false;
}

async function handleSignOut() {
    templateLoading();

    let response = await fetch(`/users/sign-out`, {
        method: "get",
        headers: getAuthorizationHeader()
    });
    let responseObject = await response.json();

    if (responseObject.status === 200) {
        clearAccessToken();
        clearQuizToken();
        pageIndex();
        return true;
    }
    if (responseObject.status === 401) {
        pageInfo401();
        return false;
    }
    pageInfo404();
    return false;
}

async function handleCreateUser() {
    const email = <HTMLInputElement>document.getElementById('input-field-email');
    const password = <HTMLInputElement>document.getElementById('input-field-password');
    const passwordRepeat = <HTMLInputElement>document.getElementById('input-field-password-repeat');
    pageLoading(false);

    if (!email) {
        pageInfo({
            errorLevel: infoBoxErrorLevel.error,
            title: "Valideringsfejl",
            message: "Du skal indtaste en email",
            buttonAction: 'pageCreateUser()',
            buttonText: 'Create User'
        });
        return;
    }

    if (password.value !== passwordRepeat.value) {
        pageInfo({
            errorLevel: infoBoxErrorLevel.error,
            title: "Valideringsfejl",
            message: "Passwords skal være forskelige",
            buttonAction: 'pageCreateUser()',
            buttonText: 'Create User'
        });
        return;
    }

    if (!password.value || !passwordRepeat.value) {
        pageInfo({
            errorLevel: infoBoxErrorLevel.error,
            title: "Valideringsfejl",
            message: "Du skal indtaste et password",
            buttonAction: 'pageCreateUser()',
            buttonText: 'Create User'
        });
        return;
    }

    let formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);

    let response = await fetch('/users', {
        body: formData,
        method: "post"
    });

    let responseObject = await response.json();

    if (responseObject.status === 201) {
        const message = "<p>Vi har nu oprettet din nye profil. Nu mangler du blot at aktivere den" +
            " via det link jeg netop har send til dig :)</p><br><p>Med venlig hilsen,</p><p>Grand Master Kwon!</p>";

        pageInfo({
            errorLevel: infoBoxErrorLevel.success,
            title: "Tillykke",
            message,
            buttonText: 'Log ind',
            buttonAction: 'pageIndex()'
        });
        return true;
    }

    pageInfo({
        errorLevel: infoBoxErrorLevel.error,
        title: "Valideringsfejl",
        message: "Emailen er allerede optaget. Måske har du glemt dit password?",
        buttonAction: 'pageCreateUser()',
        buttonText: 'Prøv igen'
    });
    return false;
}

type QuizResult = {
    timeSpent: string;
    level: string;
    percentageCorrect: number;
}

type CurrentUser = {
    email: string;
    results: QuizResult[]
}

async function handleGetCurrentUser() {

    let response = await fetch(`/users/current-user`, {
        method: "get",
        headers: getAuthorizationHeader()
    });
    let responseObject = await response.json();

    if (responseObject.status === 200) {
        const user: CurrentUser = responseObject.body;
        pageCurrentUser(user);
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