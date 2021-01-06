import getTutorial from "@/tools/tutorials/getTutorial";

const getChapterByOffset = (tutorialId, chapterId, offset) => {
    const tutorial = getTutorial(tutorialId);
    const currentChapterIndex = tutorial.chapters.findIndex(chapter => chapter.id === chapterId);
    return tutorial.chapters[currentChapterIndex + offset]
}

export default getChapterByOffset