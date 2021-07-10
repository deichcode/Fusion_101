import getChapterByOffset from "@/tools/tutorials/getChapterByOffset";

const getPreviousChapter = (tutorialId, currentChapterId) => {
    let offsetToPreviousChapter = -1;
    return getChapterByOffset(tutorialId, currentChapterId, offsetToPreviousChapter)
}

export default getPreviousChapter;