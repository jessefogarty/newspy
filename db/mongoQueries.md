**Find Articles from URL Match**
```sh
db.from_2018.find({
	link: {
		{$regex: /thestar.com/}	
	}
})
```
**Find Documents by Date Greater Than**
```
db.from_2018.findOne({
	publish_date : {
	$gt : ISODate("2018-11-01")	
	}
})`
```
*Side note: apparently mongo has a built-in method to convert str -> ISODate*

** Find documents Mongo Example **
The following query searches for movies released between January 1, 2010 and January 1, 2015. 
It includes a $limit stage to limit the output to 5 results and a $project stage to exclude all fields except title and released.

```
db.movies.aggregate([

   {

      $search: {

         "index": "releaseddate",

         "range": {

            "path": "released",

            "gt": ISODate("2010-01-01T00:00:00.000Z"),

            "lt": ISODate("2015-01-01T00:00:00.000Z")

         }

      }

   },

   {

      $limit: 5

   },

   {

      $project: {

         "_id": 0,

         "title": 1,

         "released": 1

      }

   }

])
```
