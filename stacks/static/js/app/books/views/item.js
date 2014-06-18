/**
 *  app/books/views/item.js
 *  Singular element view for a Book model
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Sun Jun 01 23:56:44 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: item.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define([
    'backbone',
    'underscore',
    'text!../tmpl/book-grid.html'
],
function(Backbone, _, bookHtml) {

    var BookGridItemView = Backbone.View.extend({
        tagName: 'div',
        className: 'col-sm-2 book-grid-item',
        template: _.template(bookHtml),

        events: {

        },

        render: function() {
            var html = this.template(this.model.toJSON());
            this.$el.html(html);
        }

    });

    return BookGridItemView;

});
