/**
 *  app/books/models/book.js
 *  The Book model for the Backbone app
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Sun Jun 01 23:46:15 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: book.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define([
    'backbone',
    'underscore'
],
function(Backbone, _) {

    var BookModel = Backbone.Model.extend({

    });

    var BookCollectionMeta = Backbone.Model.extend({

        defaults: {
            count: 0,
            next: null,
            previous: null
        }

    });

    var BookCollection = Backbone.Collection.extend({

        model: BookModel,
        url: '/api/books/',

        initialize: function() {
            this.meta = new BookCollectionMeta();
        },

        parse: function(data) {
            var results = data.results;
            delete data.results;
            this.meta.set(data);
            return results;
        },

        sync: function() {
            return Backbone.sync.apply(Backbone, arguments); // This is super!
        }

    });

    return BookCollection;

})
