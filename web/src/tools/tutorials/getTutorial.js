import tutorialsJson from '../../assets/tutorials.json'

//returns a certain tutorial form the tutorials.json file
const getTutorial = (tutorialId) => {
    const tutorials = Array.from(tutorialsJson);
    const tutorial = tutorials.find(tutorial => tutorial.id === tutorialId);
    assignEachStepUniqueId(tutorial)
    return tutorial;
}

const assignEachStepUniqueId = (tutorial) => {
    let nextStepId = 0;
    tutorial.chapters.forEach(chapter => {
        chapter.steps.forEach(step => {
            step.id = nextStepId++;
        })
    })
}

export default getTutorial;