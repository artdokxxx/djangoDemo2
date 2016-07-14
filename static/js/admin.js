requirejs.config({
    baseUrl: "/static/js/lib/",
    paths:{
        jquery: 'jquery-2.2.4.min',
        bootstrap: 'bootstrap.min',
        fuelux: 'fuelux.min',
        jasny_bootstrap: 'jasny-bootstrap.min'
    },
    shim: {
        'bootstrap': {
            deps: ['jquery']
        },
        'fuelux': {
            deps: ['bootstrap']
        },
        'jasny_bootstrap': {
            deps: ['jquery']
        }
    }
});

requirejs(['bootstrap', 'lodash'], function() {

});