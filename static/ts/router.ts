const routes = {
    '': pageIndex,
    '/': pageIndex,
    '/sign-in': pageIndex,
    '/menu': pageIndex,
    '/curriculum': ''

};

function handleRoute(): void {
    console.log('pathname');
    console.log(window.location.pathname);
    routes[window.location.pathname]();
}

function pageIndex(): void {
    const context = {title: "Dojang"};

    if (!getAccessToken()) {
        componentSignIn();
        componentTopBarSignedOut(context)
    } else {
        componentMainMenu();
        componentTopBarSignedIn(context)
    }
}
