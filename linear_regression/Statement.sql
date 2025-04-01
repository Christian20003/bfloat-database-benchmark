WITH RECURSIVE gd (idx, a, b) AS (
    SELECT 0, 1, 1
UNION ALL
    SELECT idx+1, a-0.05*avg(2*x*(a*x+b-y)), b-0.05*avg(2*(a*x+b-y))
    FROM gd, points
    WHERE idx < 5 GROUP BY idx, a, b
)
SELECT * FROM gd WHERE idx = 5;