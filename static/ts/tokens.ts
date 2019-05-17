const ACCESS_TOKEN_KEY: string = 'accessToken';
const QUIZ_TOKEN_KEY: string = 'quizToken';

function getAuthorizationHeader(): Headers {
    let headers = new Headers();
    headers.append('Authorization', getAccessToken());
    return headers
}

function getAccessToken(): string {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
}

function setAccessToken(token: string): void {
    localStorage.setItem(ACCESS_TOKEN_KEY, token)
}

function clearAccessToken(): void {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
}

function getQuizToken(): string {
    return localStorage.getItem(QUIZ_TOKEN_KEY);
}

function setQuizToken(token: string): void {
    localStorage.setItem(QUIZ_TOKEN_KEY, token)
}

function clearQuizToken(): void {
    localStorage.removeItem(QUIZ_TOKEN_KEY)

}