/**
 *  app/books/views/list.js
 *  List view for the BookCollection
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Sun Jun 01 23:50:07 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: list.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define(
function(require, exports, module) {

    var Backbone  = require('backbone');
    var _         = require('underscore');
    var BookItemView = require('./item');

    var BooksView = Backbone.View.extend({
        el: ".book-grid",

        initialize: function() {
            this.views = [];
            this.listenTo(this.collection, "sync", this.render);
            this.listenTo(this.collection, "remove", function() { this.collection.fetch(); });
            this.collection.fetch();
        },

        render: function() {

            var row = this.$('.row');

            _.invoke(this.views, "remove");
            this.views.length = 0;

            this.collection.each(function(model, idx) {
                var item = new BookItemView({ model: model });
                item.render();
                row.append(item.$el);
                this.views.push(item);
            }, this);

        },

        events: {

        }
    });

    return BooksView;

});
