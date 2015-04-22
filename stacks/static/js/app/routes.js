/**
 *  app/router.js
 *  The heart of the application, routing URLs
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Wed Jun 18 21:42:31 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: router.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

define(function(require) {

  var _ = require('underscore');
  var Backbone = require('backbone');

  var AppRouter = Backbone.Router.extend({

    routes: {
      'home': 'home',
      'books/:id': 'bookDetail',

      // Default cataches all
      '*actions': 'defaultAction'
    },

    instance: null,

    initialize: function() {

    },

    bookDetail: function(id) {
      console.log('here we are!', id);
    }

  });

  return AppRouter;
});
