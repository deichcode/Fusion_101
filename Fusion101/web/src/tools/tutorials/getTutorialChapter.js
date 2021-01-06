import getTutorial from "@/tools/tutorials/getTutorial";

const getTutorialChapter = (tutorialId, chapterId) => {
    const tutorial = getTutorial(tutorialId);
    return tutorial.chapters.find(chapter => chapter.id === chapterId);
}

export default getTutorialChapter;