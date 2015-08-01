.. _characters:

Characters
==========

**/characters/**

Lists all characters associated with the user

**/characters/add/**

Provides form to enter a Key ID and Verification Code from a user's API (EVE's user API page)

**/characters/<pk>/detail/**

Lists detailed information for one character.

``PK`` is the character's primary key (in the application's database).

**/characters/<pk>/delete/**

Deletes a single character. There is no view associated with this URI; once the request is accepted, the deletion takes place and immediately redirects user to the characters list (/characters/).

``PK`` is the character's primary key (in the application's database).

**/characters/<pk>/assets/**

Lists all assets for one character.

``PK`` is the character's primary key (in the application's database).

**/characters/<PK>/assets/update/**

Updates the character's catalog of assets. There is no view associated with this URI; once the request is accepted, the update takes place and immediately redirects user to the character's assets page (/characters/<pk>/assets/).

``PK`` is the character's primary key (in the application's database).

**/characters/<PK>/orders/**

Lists all market orders for a single character.

``PK`` is the character's primary key (in the application's database).

**/characters/<PK>/orders/update/**

Updates the character's active/expired market orders. There is no view associated with this URI; once the request is accepted, the update takes place and immediately redirects user to the character's orders page (/characters/<pk>/orders/).

``PK`` is the character's primary key (in the application's database).
