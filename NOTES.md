- Token works, 20 films per page, 1001 pages
- vote_average has 3 decimals
- Responses seem cached for about 2 hours (from the headers)
- Snapshot values for Spider-man brand-new day in 10/10/2026 :

| Time (GMT+1) | Rating | Votes |
|--------------|--------|-------|
| 12AM         | 8.364  | 4651  |
| 3:19PM       | 8.374  | 4717  |
| 5:20PM       | 8.374  | 4717  |
| 9:13PM       | 8.381  | 4771  |

- The rate limit is around 40 requests every 10 seconds
- data from 5:20 and 3:19 are the same that probably comes from no new votes or 2-hours cache
- regarding the rate limit imma wait 300ms between each request 
- there's movies with 0 votes and no rating
- movies with 0 votes are stored but excluded from predictions, since they have no rating to round
- first batch of movies and snapshots had 17 movie with 0 votes  (SELECT COUNT(*) FROM snapshots WHERE vote_count = 0;)




