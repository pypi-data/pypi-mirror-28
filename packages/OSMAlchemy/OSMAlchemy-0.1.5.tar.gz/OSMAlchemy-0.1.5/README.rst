OSMAlchemy
==========

OSMAlchemy is a bridge between SQLAlchemy and the OpenStreetMap API.

Goals
-----

OSMAlchemy's goal is to provide completely transparent integration of
the real-world OpenStreetMap data within projects using SQLAlchemy. It
provides two things:

1. Model declaratives resembling the structure of the main OpenStreetMap
   database, with some limitations, usable wherever SQLAlchemy is used,
   and
2. Transparent proxying and data-fetching from OpenStreetMap data.

The idea is that the model can be queried using SQLAlchemy, and
OSMAlchemy will either satisfy the query from the database directly or
fetch data from OpenStreetMap. That way, projects already using
SQLAlchemy do not need another database framework to use OpenStreetMap
data, and the necessity to keep a local copy of planet.osm is relaxed.

If, for example, a node with a certain id is queried, OSMAlchemy will…

-  …try to get the node from the database/ORM directly, then…
-  …if it is available, check its caching age, and…

   -  …if it is too old, refresh it from OSM, or…
   -  …else, fetch it from OSM, and…

-  …finally create a real, ORM-mapped database object.

That's the rough idea, and it counts for all kinds of OSM elements and
queries.

OSMAlchemy uses Overpass to satisfy complex queries.

Non-goals
~~~~~~~~~

OSMAlchemy does not aim to replace large-scale OSM data frameworks like
PostGIS, Osmosis or whatever. In fact, in terms of performance and
otherwise, it cannot keep up with them.

If you are running a huge project that handles massive amounts of map
data, has millions of requests or users, then OSMAlchemy is not for you
(YMMV).

OSMAlchemy fills a niche for projects that have limited resources and
cannot handle a full copy of planet.osm and an own API backend and
expect to handle limited amounts of map data.

It might, however, be cool to use OSMAlchemy as ORM proxy with an own
API backend. Who knows?

It might, as well, turn out that OSMAlchemy is an incredibly silly idea
under all circumstances.

Usage
-----

Here are a few tiny examples of how to basically use OSMAlchemy:

Installation
~~~~~~~~~~~~

OSMAlchemy can be installed just like any other standard Python package
by one of…

.. code-block:: console

    # pip3 install OSMAlchemy
    # python3 setup.py install

…or what ever kind of distribution and install system you prefer.

Using plain SQLAlchemy
~~~~~~~~~~~~~~~~~~~~~~

Make sure to get at least an engine from SQLAlchemy. Even better, get a
declarative base and a scoped session:

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, scoped_session

    engine = create_engine("sqlite:////tmp/foo.db")
    base = declarative_base(bind=engine)
    session = scoped_session(sessionmaker(bind=engine))

You can then initialise OSMAlchemy like so:

.. code-block:: python

    osmalchemy = OSMAlchemy((engine, base, session), overpass=True)

And probably install the databases:

.. code-block:: python

    base.metadata.create_all()

Using Flask-SQLAlchemy and Flask-Restless
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Imagine you have an SQLAlchemy object from Flask-SQLAlchemy bound to
your Flask application. called db, and a Flask-Restless API manager as
manager:

.. code-block:: python

    from osmalchemy import OSMAlchemy
    osm = OSMAlchemy(db, overpass=True)
    db.create_all()
    osm.create_api(manager)

You should now magically be able to query OSM via the REST API. Keep in
mind that, with no filter provided, OSMAlchemy refuses to do automatic
updates from Overpass. However, providing a query in the default JSON
query way in Flask-Restless will give you live data and cache it in the
database.

Limitations
~~~~~~~~~~~

Only some basic SQL queries are supported by the online update code.
This is because compiling SQLAlchemy's queries to OverpassQL is very
complex. If you are very good at algorithms and building compilers, feel
free to help us out!

The following kinds of queries are fully supported:

.. code-block:: python

    # A node with a specific id
    session.query(osmalchemy.node).filter_by(id=12345).one()

    # All nodes within a bounding box
    session.query(osmalchemy.node).filter(
        and_(latitude>51.0, latitude<51.1, longitude>7.0, longitude<7.1)
    ).all()

    # All nodes having a specific tag
    session.query(osmalchemy.node).filter(
        osmalchemy.node.tags.any(key="name", value="Schwarzrheindorf Kirche")
    ).all()

You can go mad combining the two with and\_() and or\_(). You can also
query for tags of ways and relations and for ways and relations by id.

Not supported (yet) are queries for ways or relations by coordinates.
You also cannot query for nodes related to a way or anything related to
a relation - having a way or a relation, accessing it will, however,
magically pull and update the nodes and members and add them to the
database:

.. code-block:: python

    # Get all nodes that are members of a (unique) named way
    session.query(osmalchemy.way).filter(
        osmalchemy.way.tags.any(key="name", value="My Unique Way")
    ).one().nodes

This should, in reality, cover most use cases. If you encounter a use
case that is not supported, please open an issue asking whether it can
be supported (if you have an idea how it can be, please add it or even
implement it and open a pull request).

Projects using OSMAlchemy
~~~~~~~~~~~~~~~~~~~~~~~~~

OSMAlchemy was designed for use in the Veripeditus Augmented Reality
framework.

Development and standards
-------------------------

Albeit taking the above into account, OSMAlchemy is developed with
quality and good support in mind. That means code shall be well-tested
and well-documented.

OSMAlchemy is tested against the following SQLAlchemy backends:

-  SQLite
-  PostgreSQL
-  MySQL

However, we recommend PostgreSQL. MySQL acts strangely with some data
and is incredibly slow, and SQLite just doesn't scale too well (however,
it is incredibly fast, in comparison).

Authors and credits
-------------------

:Authors:
    Dominik George,
    Eike Tim Jesinghaus

:Credits:
    Special thanks to Mike Bayer from SQLAlchemy for his help with
    some SQLAlchemy bugs and pitfalls, and also some heads-up.

:Contact:
    E-mail to osmalchemy@veripeditus.org

License
-------

OSMAlchemy is licensed under the MIT license. Alternatively, you are
free to use OSMAlchemy under Simplified BSD, The MirOS Licence, GPL-2+,
LGPL-2.1+, AGPL-3+ or the same terms as Python itself.
