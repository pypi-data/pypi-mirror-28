SerialAlchemy adds serialization to SQLAlchemy_ ORM objects via a mixin class. It
is tightly coupled with SQLAlchemy, because it's the best thing ever invented.


About
=====

SerialAlchemy aims to be the one serialization library that I use for web
projects. If other people like it, that's cool too. Released under the MIT License, 
so fork away!


Why create SerialAlchemy?
-------------------------

The serialization problem for web apps has been solved many times over. I had been 
using marshmallow_ for several projects. It's a great library, and has its own
`justification for existence`_.

While I liked working with marshmallow just fine, it is designed to be very broad and
fit a lot of different situations. I mostly create small web applications, so my 
situation rarely changes.

If there is one reason for creating SerialAlchemy, it is the fact that I didn't like
the idea of defining my models, then having to define marshmallow schemas. It felt
like redundancy to me. Keeping the marshmallow schema in sync with model changes
was also a pain, but feeling like I was repeating myself was the bigger reason.

And yes, "alAl" in SerialAlchemy bothers me, but SeriAlchemy sounds too much like
Siri-Alchemy, and I fear Apple's legal team.


Why not use SerialAlchemy?
--------------------------

I thought I'd take a different approach to selling this. Truth is, I made this 
library for me, and don't really care if anyone else uses it.

- SQLAlchemy is required. This library simply won't work without it.

- While SerialAlchemy is not beholden to any particular web framework, it doesn't
  make a lot of sense outside the web application area. SQLAlchemy has a 
  built-in way to `serialize expressions`_, and the result sets can be pickled.

- There is no data validation. SQLAlchemy has `simple validation`_ built-in, 
  and I feel like something more extensive is outside the scope of this project.

- SerialAlchemy is Python 3 *only*. Get used to it ;)


.. _SQLAlchemy: http://www.sqlalchemy.org
.. _marshmallow: http://marshmallow.readthedocs.org/en/latest/
.. _justification for existence: http://marshmallow.readthedocs.org/en/latest/why.html#why
.. _serialize expressions: http://docs.sqlalchemy.org/en/rel_1_0/core/serializer.html
.. _simple validation: http://docs.sqlalchemy.org/en/rel_1_0/orm/mapped_attributes.html
