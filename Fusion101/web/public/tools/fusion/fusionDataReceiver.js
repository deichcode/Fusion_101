window.fusionJavaScriptHandler = {
    handle: function (actionString, dataString) {
        console.log('Action from Fusion: ' + actionString);
        console.log('Data from Fusion: ' + dataString);

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