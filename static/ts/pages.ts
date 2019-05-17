const TITLE_CONTEXT = {title: 'Dojang'};

function pageIndex(): void {
    if (!getAccessToken()) {
        scilentRoute({data: null, title:'', url:'sign-in'});
        componentTopBarSignedOut(TITLE_CONTEXT);
        componentSignIn();
    } else {
        scilentRoute({data: null, title:'', url:'welcome'});
        componentTopBarSignedIn(TITLE_CONTEXT);
        componentMainMenu();
    }
}

function pageCreateUser(): void {
    if (!getAccessToken()) {
        scilentRoute({data: null, title: 'Hello', url: 'create-user'});
        componentTopBarSignedOut(TITLE_CONTEXT);
        componentCreateUser();
    }
    else {
        pageIndex();
    }
}

function pageCreatedUserSuccess(): void {
    scilentRoute({data: null, title:'', url:''});
    componentTopBarSignedOut(TITLE_CONTEXT);
    componentCreatedUser();
}

function pageLoading(loggedIn: boolean = true) {
    loggedIn
        ? componentTopBarSignedIn(TITLE_CONTEXT)
        : componentTopBarSignedOut(TITLE_CONTEXT);

    templateLoading()
}