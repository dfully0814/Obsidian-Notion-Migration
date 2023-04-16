#outline
# Characters
```dataviewjs
dv.table(["Name", "Backlinks", "Image"], dv.pages("#character")
	.sort(b => b.file.inlinks.length, 'desc')
	.filter(b => b.status === 'current')
	.map(b => [b.file.link, b.file.inlinks.length, '![|100](' + b.thumbnail + ')']))
```
# Notable NPCs
```dataviewjs
dv.table(["File", "Backlinks", "Image"], dv.pages("#npc")
		.sort(b => b.file.inlinks.length, 'desc')
	.filter(b => b.file.name !== "NPC" && b.file.inlinks.length >= 20 && !b.file.tags.includes("#secret"))
	.map(b => [b.file.link, b.file.inlinks.length, '![|100](' + b.thumbnail + ')']))
```

# Notable Locations
```dataviewjs
dv.table(["File", "Backlinks", "Image"], dv.pages("#location")
	.sort(b => b.file.inlinks.length, 'desc')
	.filter(b => b.file.name !== "Location" && b.file.inlinks.length >= 20 && !b.file.tags.includes("#secret"))
	.map(b => [b.file.link, b.file.inlinks.length, '![|100](' + b.thumbnail + ')']))
```

# Notable Organizations
```dataviewjs
dv.table(["File", "Backlinks", "Image"], dv.pages("#organization")
	.sort(b => b.file.inlinks.length, 'desc')
		.filter(b => b.file.name !== "Location" && b.file.inlinks.length >= 20 && !b.file.tags.includes("#secret"))
	.map(b => [b.file.link, b.file.inlinks.length, '![|100](' + b.thumbnail + ')']))
```

# Notable Lore
```dataviewjs
dv.table(["File", "Backlinks", "Image"], dv.pages("#lore")
	.filter(b => b.file.name !== "Location" && b.file.inlinks.length >= 15 && !b.file.tags.includes("#secret"))
	.sort(b => b.file.inlinks.length, 'desc')
	.map(b => [b.file.link, b.file.inlinks.length, '![|100](' + b.thumbnail + ')']))
```
