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

define([
    'jquery',
    './books/models/book',
    './books/views/list'
],
function($, BookCollection, BookListView) {

    var view = new BookListView({
        collection: new BookCollection()
    });

    return {

        view:        view,
        csrfToken:   null,
        currentUser: null,

        start: function() {
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

            console.log('Stacks App Started!');
        },

        stop: function() {
            console.log('Stacks App Stopped!');
        }

    };
});
