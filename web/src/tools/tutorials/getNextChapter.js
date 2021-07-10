import getChapterByOffset from "@/tools/tutorials/getChapterByOffset";

const getNextChapter = (tutorialId, currentChapterId) => {
    let offsetToNextChapter = 1
    return getChapterByOffset(tutorialId, currentChapterId, offsetToNextChapter)
}

export default getNextChapter;