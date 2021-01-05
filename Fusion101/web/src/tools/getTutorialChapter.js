import getTutorial from "@/tools/getTutorial";

const getTutorialChapter = (tutorialId, chapterId) => {
    const tutorial = getTutorial(tutorialId);
    console.log(chapterId)
    console.log(tutorial.chapters.find(chapter => chapter.id === chapterId))
    return tutorial.chapters.find(chapter => chapter.id === chapterId);
}

export default getTutorialChapter;