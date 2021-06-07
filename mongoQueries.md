**Find Articles from URL Match**
```sh
db.from_2018.find({
	link: {
		{$regex: /thestar.com/}	
	}
})
```
