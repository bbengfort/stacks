/**
 *  app/main.js
 *  The main entry point to the single page app
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Sun Jun 01 23:28:51 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: main.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define(function(require) {

    var $ = require('jquery');
    var BookCollection = require('./books/models/book');
    var BookListView   = require('./books/views/list');
    var AppRouter      = require('./routes');

    var view = new BookListView({
        collection: new BookCollection()
    });

    var App = new function() {

        this.view        = view;
        this.csrfToken   = null;
        this.currentUser = null;
        this.routes      = new AppRouter();

        this.start = function() {
            this.csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            this.currentUser = "http://127.0.0.1:8000/api/users/1/";

            // Setup the X-CSRF header
            $.ajaxSetup({headers: {"X-CSRFToken": this.csrfToken}});

            // Add the hotkeys to the document
            $(document).keyup(function(e) {

                if (e.keyCode == 27) {
                    e.preventDefault();
                    window.location = "/admin/";
                }

            });

            // Start the history for the router
            Backbone.history.start();

            console.log('Stacks App Started!');
        }

        this.stop = function() {
            console.log('Stacks App Stopped!');
        }

    };

    return App
});
