const getTutorialMedia = (tutorialId, fileName) => {
      return require(`@/assets/tutorials/${tutorialId}/${fileName}`) //https://github.com/vuejs/vue-loader/issues/896
}

export default getTutorialMedia;