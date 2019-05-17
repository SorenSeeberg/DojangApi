const routes = {
    '/': pageIndex,
    '/sign-in': pageIndex,
    '/welcome': pageIndex,
    '/create-user': pageCreateUser,
    '/curriculum': ''

};

// pageLoading

function handleRoute(): void {
    console.log('pathname');
    console.log(window.location.pathname);
    routes[window.location.pathname]();
}

type Url = {
    data: any;
    title: string;
    url: string;
}

function scilentRoute(url: Url): void {
    const values = [...Object.keys(url).map(k => url[k])];
    console.log(values);

    history.replaceState(url.data, url.title, url.url);
    // history.pushState(url.data, url.title, url.url);
}