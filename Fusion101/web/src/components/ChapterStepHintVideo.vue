<template>
  <div class="hint">
    <video class="hint-video" :class="{'hint-video--hidden': isHidden }" ref="hintVideo" poster="@/assets/images/hint-video-placeholder.png">
    </video>
  </div>
</template>

<script>
import getTutorialMedia from "@/tools/tutorials/getTutorialMedia";
import sleep from "@/tools/sleep";

export default {
  name: "ChapterStepHintVideo",
  props: {
    hint: String,
    storeRef: Function
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
      videoFormats: ["mp4", "webm"],
      isHidden: false
    }
  }, mounted() {
    this.passDomReferenceToParent.call(this);
    this.restartVideoWhenEnded.call(this);
  },
  methods: {
    passDomReferenceToParent() {
      if (this.storeRef) {
        this.storeRef(this.$refs.hintVideo)
      }
    },
    restartVideoWhenEnded() {
      this.$refs.hintVideo.addEventListener('ended', async () => {
        await this.restartVideo();
      });
    },
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
      try {
        return getTutorialMedia(this.tutorialId, fileName)
      } catch (e) {
        return ""
      }
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
      this.isHidden = true
      await sleep(300)
    },
    setVideoToStart() {
      this.$refs.hintVideo.currentTime = 0
    },
    showVideo: async function () {
      this.isHidden = false
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
@import "src/css/variables/colors";

.hint {
  width: 100%;
  height: calc((100vw) * 0.42);
  background-color: $white;
  border-bottom: 1px solid $active;
  border-top: 1px solid $active;
  overflow: hidden;

  .hint-video {
    opacity: 1;
    transition: opacity 300ms;
    width: 100%;

    &.hint-video--hidden {
      opacity: 0;
    }
  }
}
</style>