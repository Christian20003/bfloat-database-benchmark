STATEMENT =  '''
WITH RECURSIVE gd (id, w_xh, w_ho) AS (
   SELECT * FROM weights
   UNION ALL
   SELECT id+1, w_xh - {} * {}(transpose(img)**d_xh), w_ho - {} * {}(transpose(a_xh)**d_ho)
   FROM (
      SELECT l_xh * a_xh * (1-a_xh) AS d_xh, *
      FROM (
         SELECT d_ho**transpose(w_ho) AS l_xh, *
         FROM (
            SELECT (l_ho * a_ho * (1-a_ho)) AS d_ho, *
            FROM (
               SELECT 2*(a_ho-one_hot) AS l_ho, *
               FROM (
                  SELECT sig(a_xh**w_ho) AS a_ho, *
                  FROM (
                     SELECT sig(img**w_xh) AS a_xh, *
                     FROM (SELECT * FROM iris3) data, gd WHERE id < {}
                  ) input_hidden
               ) hidden_output
            ) derivative_loss
         ) derivative_sig1 
      ) derivative_mul
   ) derivative_sig2
   GROUP BY id, w_ho, w_xh), 
accuracy AS (
SELECT id, correct, count(*) AS count FROM (
   SELECT id, highestposition(sig(sig(img**w_xh)**w_ho))=highestposition(one_hot) AS correct FROM iris3, gd
) result 
GROUP BY id, correct)
SELECT id, count*1.0/(SELECT SUM(count) FROM accuracy t2 WHERE t1.id=t2.id ) 
FROM accuracy t1 
WHERE correct=true;'''

STATEMENT_WEIGHTS = '''
WITH RECURSIVE gd (id, w_xh, w_ho) AS (
   SELECT * FROM weights
   UNION ALL
   SELECT id+1, w_xh - {} * {}(transpose(img)**d_xh), w_ho - {} * {}(transpose(a_xh)**d_ho)
   FROM (
      SELECT l_xh * a_xh * (1-a_xh) AS d_xh, *
      FROM (
         SELECT d_ho**transpose(w_ho) AS l_xh, *
         FROM (
            SELECT (l_ho * a_ho * (1-a_ho)) AS d_ho, *
            FROM (
               SELECT 2*(a_ho-one_hot) AS l_ho, *
               FROM (
                  SELECT sig(a_xh**w_ho) AS a_ho, *
                  FROM (
                     SELECT sig(img**w_xh) AS a_xh, *
                     FROM (SELECT * FROM iris3) data, gd WHERE id < {}
                  ) input_hidden
               ) hidden_output
            ) derivative_loss
         ) derivative_sig1 
      ) derivative_mul
   ) derivative_sig2
   GROUP BY id, w_ho, w_xh)
SELECT * FROM gd;'''