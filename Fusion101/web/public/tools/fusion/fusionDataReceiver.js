//receive messages from python part of the fusion 360 plugin
window.fusionJavaScriptHandler = {
    handle: function (actionString, dataString) {
        const event = new CustomEvent("Fusion360Message", {
            detail: {
                action: actionString,
                data: dataString
            }
        });
        window.dispatchEvent(event);

        const result = {};
        result.status = 'OK';
        return JSON.stringify(result);
    }
};