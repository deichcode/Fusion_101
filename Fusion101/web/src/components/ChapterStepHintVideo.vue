<template>
  <video class="hint" ref="hintVideo"/>
</template>

<script>
import getTutorialMedia from "@/tools/tutorials/getTutorialMedia";
import sleep from "@/tools/sleep";

export default {
  name: "ChapterStepHintVideo",
  props: {
    hint: String
  },
  watch: {
    'hint': function () {
      if (this.$props.hint) {
        this.showHint(this.$props.hint)
      } else {
        this.hideHint();
      }
    }
  },
  data() {
    return {
      tutorialId: this.$route.params.tutorialId,
      videoFormats: ["mp4", "webm"]
    }
  }, mounted() {
    this.$refs.hintVideo.addEventListener('ended', async () => {
      await this.restartVideo();
    });
  },
  methods: {
    showHint(hint) {
      this.videoFormats.forEach(format => {
        let videoFilename = `${hint}.${format}`;
        let sourceElement = this.createSourceElementFor(videoFilename);
        this.addSourceToHintVideo(sourceElement);
      })
      this.playVideo()
    },
    createSourceElementFor: function (hint) {
      let sourceElement = document.createElement('source')
      let videoSrc = this.getVideoSrc(hint)
      sourceElement.setAttribute('src', videoSrc)
      return sourceElement;
    },
    getVideoSrc(fileName) {
      return getTutorialMedia(this.tutorialId, fileName)
    },
    addSourceToHintVideo: function (sourceElement) {
      this.$refs.hintVideo.appendChild(sourceElement)
    },

    hideHint() {
      this.removeVideoSource();
      this.stopAndHideVideo();
    },
    removeVideoSource() {
      this.$refs.hintVideo.innerHTML = '';
    },
    stopAndHideVideo() {
      this.$refs.hintVideo.pause();
      this.$refs.hintVideo.load();
    },

    restartVideo: async function () {
      await this.hideVideo();
      this.setVideoToStart();
      await this.showVideo();
      this.playVideo();
    },
    hideVideo: async function () {
      this.$refs.hintVideo.classList.add('hint--hidden')
      await sleep(300)
    },
    setVideoToStart() {
      this.$refs.hintVideo.currentTime = 0
    },
    showVideo: async function () {
      this.$refs.hintVideo.classList.remove('hint--hidden')
      await sleep(200)
    },

    playVideo() {
      this.$refs.hintVideo
          .play()
          .catch(() => {
            //Fast hovering removes source before play could finished which results in rejected promise
            //No need to handle this
          })
    },
  }
}
</script>

<style lang="scss" scoped>
.hint {
  transition: opacity 300ms;
  opacity: 1;
  width: 100%;
  height: calc((100vw - 10px) * 0.4286);

  &.hint--hidden {
    opacity: 0;
  }
}
</style>