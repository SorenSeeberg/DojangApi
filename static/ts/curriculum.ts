
type CurriculumRow = string[]

type Curriculum = {
    levelMaxLabel: string;
    levelMinLabel: string;
    levelLabels: string[];
    categoryLabel: string;
    categoryLabels: string[];
    data: CurriculumRow[];
}

async function handleGetCurriculum(categoryId: number, levelMin: number, levelMax: number) {
    templateLoading();

    let response = await fetch(`/curriculum?categoryId=${categoryId}&levelMin=${levelMin}&levelMax=${levelMax}`, {
        method: 'get',
        headers: getAuthorizationHeader()
    });

    let responseObject = await response.json();

    if (responseObject.status === 200){
        console.log(responseObject);
        const curriculum: Curriculum = responseObject.body;
        pageCurriculum(curriculum);
        return true;
    }

    return false;
}