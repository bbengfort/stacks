# Stacks
**Personal eBook library for the Bengfort Family**

[![Build Status][travis_img]][travis_href]
[![Coverage Status][coverage_img]][coverage_href]
[![Stories in Ready][waffle_img]][waffle_href]

[![My favorite book shop](docs/img/stacks.jpg)][stacks.jpg]

## How to Run

In order to run the server locally, follow these steps:

1. Clone the repository into a working directory of your choice
2. Install the dependencies using pip install -r requirements.txt
    Note, it may be helpful to use a virtualenv
3. Set the following environment vars:

        $ export DJANGO_SETTINGS_MODULE=stacks.settings.development
        $ export SECRET_KEY="super secret pass"
        $ export GOOGLE_OAUTH2_KEY="googlekey"
        $ export GOOGLE_OAUTH2_SECRET="googlesecret"

    Note that this app is enabled with Google OAuth login, you'll need to
    create your own Google credentials with the Google Developers console.

4. Create a database on postgres (on the localhost) called stacks
    Note, you can set the envvars DB_NAME, DB_USER, DB_PASS etc.
5. Run the database migration:

        $ python stacks/manage.py migrate

6. Run the server:

        $ make runserver

7. You should now be able to open a browser at http://127.0.0.1:8000

## About

The Bengfort Stacks is a content and media storage facility for the Bengfort family to keep and backup DRM free eBooks for personal use. The site is login only and is intended only to facilitate backup of media owned by the users of the site.

### Contributing

Stacks is open source, but because this is a personal project, I would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute, you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/bbengfort/stacks/issues](https://github.com/bbengfort/stacks/issues)
2. Work on a card on the dev board: [https://waffle.io/bbengfort/stacks](https://waffle.io/bbengfort/stacks)
3. Create a pull request in Github: [https://github.com/bbengfort/stacks/pulls](https://github.com/bbengfort/stacks/pulls)

The repository is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/bbengfort/stacks) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

### Attribution

The image used in this README, &ldquo;[My favorite book shop][stacks.jpg]&rdquo; by [Bravo\_Zulu\_](https://www.flickr.com/photos/76686348@N05/) is licensed under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)


<!-- References -->
[travis_img]: https://travis-ci.org/bbengfort/stacks.svg
[travis_href]: https://travis-ci.org/bbengfort/stacks
[waffle_img]: https://badge.waffle.io/bbengfort/stacks.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/bbengfort/stacks
[coverage_href]: https://coveralls.io/r/bbengfort/stacks
[coverage_img]: https://coveralls.io/repos/bbengfort/stacks/badge.svg?branch=develop
[stacks.jpg]: https://flic.kr/p/daqcX7
