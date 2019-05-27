type CurriculumRow = string[]

type Curriculum = {
    levelMaxLabel: string;
    levelMinLabel: string;
    levelLabels: string[];
    categoryLabel: string;
    categoryLabels: string[];
    data: CurriculumRow[];
}

async function handleUpdateCurriculumFromForm() {
    const select0 = <HTMLSelectElement>document.getElementById('select-curriculum-category');
    const select1 = <HTMLSelectElement>document.getElementById('select-curriculum-level-min');
    const select2 = <HTMLSelectElement>document.getElementById('select-curriculum-level-max');

    const categoryId: number = select0.selectedIndex;
    const levelMin: number = select1.selectedIndex + 1;
    const levelMax: number = select2.selectedIndex + 1;

    await handleGetCurriculum(categoryId, levelMin, levelMax);
}

async function handleGetCurriculum(categoryId: number, levelMin: number, levelMax: number) {
    templateLoading();

    let response = await fetch(`/curriculum?categoryId=${categoryId}&levelMin=${levelMin}&levelMax=${levelMax}`, {
        method: 'get',
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200) {
        if (DEV) {
            console.log(responseObject);
        }
        const curriculum: Curriculum = responseObject.body;
        pageCurriculum(curriculum);
        return true;
    }

    if (responseObject.status === 401) {
        pageInfo401();
        clearQuizToken();
        clearAccessToken();
        return false;
    }

    pageInfo404();
    return false;
}