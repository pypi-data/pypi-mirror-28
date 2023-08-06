BreezeBlocks
============

BreezeBlocks is a query abstraction layer that takes advantage of some of the
features of the Python language more than DBAPI 2.0 modules, but provides
more lightweight result objects and more flexible querying than many ORMs for
the language.

Most available SQL abstractions are ORMs implementing something similar to
the Active Record pattern. A class is defined for each table,  with class-level
properties representing the columns. Rows in the table become instances of their
class.

BreezeBlocks is designed as a query builder rather than an ORM. SQL Syntax is
exposed in Python classes which are passed into methods for query construction.
Query results are plain-old-data types similar to a C struct. They provide
access to fields of the row by name, but are still compact and don't have as
much usage overhead as most Python objects.

This package is meant to help you use databases, not manage databases. The
current focus of the project is on querying. Functionality for insertion,
updating, and deleting are expected to be developed in time. However, defining
schemas and creating tables are not with the scope of the project.

Version History
===============
0.2.1
-----
Adding DML functionality. New builders and new operations for database inserts,
updates, and deletes have been added. They are accessible from the Database
class just like the query builder.

The new builders use a similar interface to the query builder, and the new
operations use a similar interface to the query.

0.2.0
-----
Divide the responsibilities of building and representing a query between two
classes, Query and the new QueryBuilder.

If upgrading from a previous version, please review the Query and QueryBuilder
classes. When building a query, query_builder.get() must now be invoked to
get a usable query object.

0.1.1
-----
Introduces the Column Collection concept to the code, and starts using its
implementation in tables, joins, and queries.

0.1.0
-----
Query functionality covers enough possibilities of the SQL language to meet
most anticipated developer needs.
