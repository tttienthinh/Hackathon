MERGE (p:Character {name:"Aegon-I-Targaryen"})-[:LIKES {date:2002}]->(t:Character {name: "Daenerys-Targaryen"})  

https://github.com/neo4j-contrib/neovis.js  

MATCH p=(:Character)-[l:LIKES]-(c:Character) delete l,c,p   

Installer neo4J sur linux en ligne de commandes :  
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04  
cypher-shell  
```
cypher-shell -a 'neo4j://your_hostname:7687'
```

port forward pagekite
https://pagekite.net/  


https://stackoverflow.com/questions/42740355/how-to-install-apoc-for-neo4j  



