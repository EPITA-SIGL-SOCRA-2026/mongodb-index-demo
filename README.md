# Importance des indexes pour une base de données

**Objectif :** Comprendre l'importance des indexes dans une base de données en utilisant MongoDB.

**Démarche :** Mettre en place un environnement MongoDB, générer des données de cultures et de commentaires, et exécuter des requêtes pour observer les performances avec et sans indexes:

1. Configuration de l'environnement
2. Execution des requêtes
   - Requêtes sans index
   - Requêtes avec index
   - Comparaison des performances

## Configuration de l'environnement

1. **Configuration de MongoDB :** lancer MongoDB en utilisant Docker et le fichier `docker-compose.yml` fourni.
   ```bash
   docker compose up -d
   ```
2. **Générer des données :** exécuter le script `generate_cultures_comments.py` pour générer des données de cultures et de commentaires.
   ```bash
   # Python 3 doit être installé
   pip install -r requirements.txt
   python generate_cultures_comments.py --nb-jardins 100000 --nb-plantes 156 --nb-jardiniers 500
   ```
3. **Importer les données dans MongoDB:** utiliser `mongoimport` pour importer les données générées dans la base de données MongoDB.
   ```bash
   # Importation des données dans la collection "commentaires" de la base de données "demo"
   docker compose exec -it mongodb mongoimport -u root -p example --db demo --collection commentaires --file=/opt/commentaires.json --jsonArray --authenticationDatabase=admin
   ```

> Note: Voici le format d'un document dans la collection `commentaires` :

```javascript
{
  _id: ObjectId('68772d35686990875e1167aa'),
  jardin_id: 0,
  plante_id: 71,
  commentaires: [
    {
      jardinier_id: 438,
      message: 'Bonne croissance en sol sableux',
      date: '2025-03-19T17:39:53.075940'
    }
  ]
}
```

## Exécution des requêtes

1. **Sans indexes :** Compter le nombre de commentaires pour la plante avec l'id `42` et mesurer les statistiques d'exécution.:
   ```javascript
   db.commentaires
     .explain("executionStats")
     .aggregate([
       { $match: { plante_id: 42 } },
       { $unwind: "$commentaires" },
       { $group: { _id: null, count: { $sum: 1 } } },
     ]).stages[0].$cursor.executionStats;
   ```
   Voici un exemple de résultat :

```javascript
{
  executionSuccess: true,
  nReturned: 18003,
  executionTimeMillis: 775,
  totalKeysExamined: 0,
  totalDocsExamined: 2845208,
  executionStages: {
    // ...,
  }
}
```

2. Créer un index sur le champ `plante_id` :

   ```javascript
   db.commentaires.createIndex({ plante_id: 1 });
   ```

   > Note: Le temps peux devenir relativement long pour créer l'index, en fonction du nombre de documents dans la collection. Il s'agit du temps nécessaire pour analyser tous les documents de la collection et construire l'index.

3. **Avec index :** Refaire la même requête et mesurer les statistiques d'exécution :
   ```javascript
   db.commentaires
     .explain("executionStats")
     .aggregate([
       { $match: { plante_id: 42 } },
       { $unwind: "$commentaires" },
       { $group: { _id: null, count: { $sum: 1 } } },
     ]).stages[0].$cursor.executionStats;
   ```
   Voici un exemple de résultat :

```javascript
{
  executionSuccess: true,
  nReturned: 18003,
  executionTimeMillis: 56,
  totalKeysExamined: 18003,
  totalDocsExamined: 18003,
  executionStages: {
    // ...,
  }
}
```

**Resultats :**

|            | Nombre de documents examinés | Temps d'exécution |
| ---------- | ---------------------------- | ----------------- |
| Sans index | 2,845,208                    | 775 ms            |
| Avec index | 18,003                       | 56 ms             |

- **Sans index :** tous les documents examinés, la requête prend plus de temps. Ici `totalDocsExamined` est de 2,845,208 et `executionTimeMillis` est de 775 ms.
- **Avec index :** uniquement les documents pertinents examinés, la requête est beaucoup plus rapide. Ici `totalDocsExamined` est de 18,003 et `executionTimeMillis` est de 56 ms.
- **Conclusion :** L'utilisation d'index améliore significativement les performances des requêtes, soit un rapport de **13,8x** dans cet exemple.
