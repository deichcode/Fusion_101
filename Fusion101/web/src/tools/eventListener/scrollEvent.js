export const executeOnScroll = (callback) => {
    document.addEventListener('scroll', () => {
        callback.call()
    });
}