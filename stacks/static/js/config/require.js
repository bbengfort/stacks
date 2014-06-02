/**
 *  config/require.js
 *  Configures the require.js lookup paths
 *
 *  Author:   Benjamin Bengfort <ben@cobrain.com>
 *  Created:  Sun Jun 01 23:25:33 2014 -0400
 *
 *  Copyright (C) 2014 Cobrain Company
 *  For license information, see LICENSE.txt
 *
 *  ID: require.js [] ben@cobrain.com $
 */

// JS Hint directives and strict mode
/* globals exports,__filename */
'use strict';

requirejs.config({
  baseUrl: '/static/js',
  urlArgs: '?v=' + new Date().getTime(),
  paths: {
    'backbone': 'libs/backbone',
    'underscore': 'libs/underscore',
    'jquery': 'libs/jquery',
    'bootstrap': 'libs/bootstrap',
    'text': 'libs/require-text'
  },
  shim: {
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'underscore': {
      exports: '_'
    },
    'jquery': {
      exports: '$'
    },
    'bootstrap': {
      deps: ['jquery']
    }
  }
});
