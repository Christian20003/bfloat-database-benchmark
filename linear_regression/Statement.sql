WITH RECURSIVE gd (id, a, b) AS (
    SELECT 0, 1::float, 1::float
UNION ALL
    SELECT id+1, a-0.05*avg(2*x*(a*x+b-y)), b-0.05*avg(2*(a*x+b-y))
    FROM gd, points
    WHERE id < 10 GROUP BY id, a, b
)
SELECT * FROM gd WHERE id = 10;