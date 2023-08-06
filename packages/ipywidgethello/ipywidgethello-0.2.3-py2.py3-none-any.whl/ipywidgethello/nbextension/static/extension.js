define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                'jupyter-widget-hello': 'nbextensions/jupyter-widget-hello/index',
            },
        }
    });
    // Export the required load_ipython_extention
    return {
        load_ipython_extension : function() {}
    };
});
