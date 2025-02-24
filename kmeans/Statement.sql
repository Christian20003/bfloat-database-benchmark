WITH RECURSIVE 
points_start (pid, x, y) AS (SELECT * FROM points),
clusters_start (cid, x, y) AS (SELECT * FROM clusters_0),
clusters (iter, cid, x, y) AS (
    (SELECT 0,* FROM clusters_start)
    UNION ALL
    SELECT iter+1,cid, AVG(px), AVG(py) FROM (
        SELECT iter, pid, p.x AS px, p.y AS py, MIN(cid) AS cid
        FROM points_start p, clusters c
        WHERE NOT EXISTS (
            SELECT * FROM clusters d
            WHERE c.iter = d.iter AND (d.x-p.x)^2 + (d.y-p.y)^2 < (c.x-p.x)^2 + (c.y-p.y)^2
        )
        GROUP BY iter, pid, p.x, p.y
    ) AS result
    WHERE iter<10
    GROUP BY cid, iter
)
SELECT * FROM clusters WHERE iter = 10 ORDER BY cid;
