# Extracted Notes - Database

## Table of Contents

- [Overview](#overview)
- [Queries](#queries)
- [Cursor](#cursor)
- [Indexing](#indexing)

## Overview

- BSON - MongoDB represents JSON documents in binary form called BSON internally. It enriches JSON with additional data types that Mongo uses like Object Id, date, etc.

- Mongo DB is schema-less. Mongo does not enforces a schema, but documents inside the same collection should have a similar structure for consistency.

- CAP Theorem - consistency, availability, partition tolerance (system won't fail). MongoDB supports consistency and partition tolerance.

- Types of NoSQL databases - relational database, document database, key-value databases (Redis DB), white-column stores (Cassandra DB), Graph Database

- MongoDB is a document database.

- Why use MongoDB - open source, document database, high performance, rich query language, high availability, horizon scalability.

- JSON is a UTF-8 String but BSON is a Binary. JSON is human and machine readable but BSON is a machine readable only.

- MongoDB is a case-sensitive language. It supports MongoDB query language (MQL). It has dynamic JSON based schema unlike predefined in MySQL. It has no foreign keys or joins or triggers. It follows CAP theorem not ACID properties. It is horizontal scalable unlike SQL which have vertical scalable.

- Which is best database - is your data structured or unstructured? preferred scalability strategy? No need for ORM (object relational mappings) with MongoDB.

- There is no schema enforcement from MongoDB, it is a application responsibility.

- By using the BSON and memory mapped files concept to store the data, makes the MongoDB very fast and efficient.

- The `_id` can contains any type of data except array. We cannot replace the `_id` value with another value.

- The ObjectId() will return a new object id and it also contains a timestamp ObjectId().getTimestamp() in ISODate format. We can use it for sorting in created by format.

- Replicate sets - Minimum replica sets in MongoDB - primary db (only writable instance), secondary db (read-only instances, data is replicated from primary db) and arbiter db (no data, provides additional vote to elect the db in-case if primary gets failed).

- History of database -

  ![database-history](./images/database-history.png)

## Queries

- The find() method returns a cursor to the documents that match the query criteria. In projection, 1 means inclusion and 0 for exclusion.

  ```typescript
  db.aircraft.find({}, { model: 1, range: 1, _id: 0 });
  db.aircraft.find().pretty();
  db.aircraft.find().count();
  db.aircraft.find().skip(3);
  db.aircraft.find().limit(5);
  db.aircraft.find().sort({ model: 1 });
  ```

- Logical Query Operators - $and and $or.

  ```typescript
  db.aircraft.find({ $and: [{ capacity: 124 }, { range: { $gt: 6000 } }] });
  db.aircraft.find({ range: { $lt: 600, $gt: 6000 } }); // short-hand syntax if same field
  ```

- Mongo DB does not guarantee the order of the returned documents unless sort() method is used. 1 for the ascending order and -1 for descending order.

- Comparison query operations - $eq, $ne, $in, $nin, $lt, $lte, $gt, $gte

  ```typescript
  db.aircraft.find({model: 'Boeing'})
  db.aircraft.findOne({model: 'Boeing'})
  db.aircraft.findOne({model: {$ne: 'Boeing'}})
  db.aircraft.findOne({model: {$in: ['Boeing', 'Airbus]}})
  db.aircraft.findOne({model: {$in: [/^A/]}}) // using regular expression
  ```

- To know about how MongoDB will find the document, we can use explain() method -

  ```typescript
  db.animals.find({ name: 'cat' }).explain();
  ```

## Cursor

- Cursor - A virtual object where MongoDB stores the documents returned by the find method. It can have any methods like below -

- The find() method returns a cursor, however the findOne() method returns an actual document. If no document match the criteria, the method returns null.

- MongoDB uses a cursor to support the efficient retrieval of the document as documents might be in huge number which might support the memory to load. By this, it will give you a batch of documents and close the connection.

## Indexing

- We can use index to speed up the queries. The scanning of each location on the disk is bad for performance which finding a record, the solution is to use an index, it basically holds mapping to those locations from field values. By this, we can jump directly to the disk location where document is stored is good for performance and less i/o operations. It also good for sorting performance purpose as-well. Without index it will show n number of objects has been scanned, after index it will show 1 number od object has been scanned. Index on the `_id` field can not be dropped.

- Index types - Regular (B-tree), Geo (sort nearby locations), Text, Hashed, TTL (expiration date for documents)

- Covering index - we use query using index and all the information is with index itself then there is no need to go to the dist to get the actual document, we can use the index itself to the actual result. In the explain() it will say indexOnly as true. Suppose we have applied index on name field and returning only the name field, not even `_id`, then the covering index will be used.

- When our database is large, we can create index in the background so that read and write action won't get blocked.
