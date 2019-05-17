async function handleSignIn() {

    // pageLoading(false);

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

    templateSignInError();
    return false;
}

async function handleCreateUser() {
    const email = <HTMLInputElement>document.getElementById('input-field-email');
    const password = <HTMLInputElement>document.getElementById('input-field-password');
    const passwordRepeat = <HTMLInputElement>document.getElementById('input-field-password-repeat');

    if (password.value !== passwordRepeat.value){
        // todo : pageCreatedUserError();
        return;
    }

    pageLoading(false);

    let formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);

    let response = await fetch('/users', {
        body: formData,
        method: "post"
    });

    let responseObject = await response.json();

        if (responseObject.status === 201) {
            pageCreatedUserSuccess();
            return true;
    }

    // todo : pageCreatedUserError();
    return false;
}