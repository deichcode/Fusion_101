var adsk = window.adsk = window.adsk || {};
adsk.fusionSendData = function(action, data) {
    var result;
    try {
        result = neutronJavaScriptObject.executeQuery(action, data);
    } catch (e) {
        result = e.toString();
    }
    return result;
};