import getTutorial from "@/tools/tutorials/getTutorial";

//returns the chapter from the array of chapters with the index that is higher by the offset than the index of the given chapter id
const getChapterByOffset = (tutorialId, chapterId, offset) => {
    const tutorial = getTutorial(tutorialId);
    const currentChapterIndex = tutorial.chapters.findIndex(chapter => chapter.id === chapterId);
    return tutorial.chapters[currentChapterIndex + offset]
}

export default getChapterByOffset