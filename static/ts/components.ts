console.log('We are live');

console.log('Even more love');

function yep(): string {
    let hello = 6;
    console.log(`Hello ${hello}`);
    return "Meh"
}

function componentHeader(loggedIn: boolean = true): void {

    let title = "DOJANG";

    let headerElement: HTMLElement = document.getElementById('header');

    if (loggedIn) {
        headerElement.innerHTML = `<div>${title}</div><div class='header-profile'/>`
    } else {
        headerElement.innerHTML = `<div>${title}</div>`
    }
}

function componentSignIn() {

    let articleElement: HTMLElement = document.getElementById('article');

}