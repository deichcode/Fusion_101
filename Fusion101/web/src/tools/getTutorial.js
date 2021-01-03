import tutorialsJson from '../assets/tutorials.json'

const getTutorial = (tutorialId) => {
    const tutorials = Array.from(tutorialsJson);
    return tutorials.find(tutorial => tutorial.id === tutorialId);
}

export default getTutorial;