Mongotime is a sampling-based performance analysis tool for MongoDB that aims
to give you a deep view into how Mongo is spending its time by showing %
utilization of various activity types, and allowing you to add custom grouping
and filtering.

This approach is particularly useful if your DB is strained by a high volume of
fast queries, rather than a few slow ones. Besides optimizing slow queries, you
might want to understand and change general access patterns. For example, maybe
your DB is spending way too much time looking up a user's last login time, even
if each lookup is very fast because of indexing.

See the project page on github: https://github.com/heewa/mongotime


