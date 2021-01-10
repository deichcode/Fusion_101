import getTutorial from "@/tools/tutorials/getTutorial";

//load chapter with chapterId from the tutorial with tutorialId and return as object
const getTutorialChapter = (tutorialId, chapterId) => {
    const tutorial = getTutorial(tutorialId);
    return tutorial.chapters.find(chapter => chapter.id === chapterId);
}

export default getTutorialChapter;