CONFIG = {
    'iterations': [10],
    'types': ['float', 'tfloat'],
    'learning_rate': 0.01,
    'setup1': {
        'network_size': 20,
        'data_size': 150
    },
    'setup2': {
        'network_size': 20,
        'data_size': 300
    },
    'setup2': {
        'network_size': 20,
        'data_size': 600
    },
    'setup3': {
        'network_size': 20,
        'data_size': 1200
    },
    'setup4': {
        'network_size': 50,
        'data_size': 150
    },
    'setup5': {
        'network_size': 50,
        'data_size': 300
    },
    'setup6': {
        'network_size': 50,
        'data_size': 600
    },
    'setup7': {
        'network_size': 50,
        'data_size': 1200
    }
}
CTE = '''
WITH RECURSIVE weights_now (iter, layer, input, output, value) AS (
  (SELECT 0 AS iter, 0 AS layer, intput, output, value FROM weights_layer1_layer2 UNION SELECT 0 AS iter, 1 AS layer, input, output, value FROM weights_layer2_layer3)
  UNION ALL
  (
  WITH a_xh(sample_id, output, value) AS (
     SELECT sample_id, output, 1 / (1 + exp(-1 * result)) AS value
     FROM (SELECT m.sample_id, n.output, SUM(m.value * n.value) AS result
            FROM data AS m INNER JOIN weights_now AS n ON m.feature_id = n.input
            WHERE m.sample_id < {} AND n.layer = 0 AND n.iter = (SELECT MAX(iter) from weights_now) -- w_xh
            GROUP BY m.sample_id, n.output) calculation_1
  ), a_ho(sample_id, output, value) AS (
     SELECT sample_id, output, 1 / (1 + exp(-1 * result)) AS value
     FROM (SELECT m.sample_id, n.output, SUM(m.value * n.value) AS result --sig(SUM (m.v*n.v))
            FROM a_xh AS m INNER JOIN weights_now AS n ON m.output = n.input
            WHERE n.layer = 1 AND n.iter = (SELECT MAX(iter) FROM weights_now)  -- w_ho
            GROUP BY m.sample_id, n.output) calculation_2
  ), l_ho(sample_id, output, value) AS (
     SELECT m.sample_id, m.output, 2 * (m.value - n.isValid)
     FROM a_ho AS m INNER JOIN one_hot AS n ON m.sample_id = n.sample_id AND m.output = n.species_id
  ), d_ho(sample_id, output, value) AS (
     SELECT m.sample_id, m.output, m.value * n.value * (1 - n.value)
     FROM l_ho AS m INNER JOIN a_ho AS n ON m.sample_id = n.sample_id AND m.output = n.output
  ), l_xh(sample_id, output, value) AS (
     SELECT m.sample_id, n.input as output, SUM(m.value * n.value) -- transpose
     FROM d_ho AS m INNER JOIN weights_now AS n ON m.output = n.output
     WHERE n.layer = 1 AND n.iter = (SELECT MAX(iter) FROM weights_now)  -- w_ho
     GROUP BY m.sample_id, n.input
  ), d_xh(sample_id, output, value) AS (
     SELECT m.sample_id, m.output, m.value * n.value * (1 - n.value)
     FROM l_xh AS m INNER JOIN a_xh AS n ON m.sample_id = n.sample_id AND m.output = n.output
  ), d_w(layer, input, output, value) AS (
     SELECT 0, m.feature_id as input, n.output, SUM(m.value * n.value)
     FROM data AS m INNER JOIN d_xh AS n ON m.sample_id = n.sample_id
     WHERE m.sample_id < {}
     GROUP BY m.feature_id, n.output
     UNION
     SELECT 1, m.output as input, n.output, SUM(m.value * n.value)
     FROM a_xh AS m INNER JOIN d_ho AS n ON m.sample_id = n.sample_id
     GROUP BY m.output, n.output
  )
  SELECT iter + 1, w.layer, w.input, w.output, w.value - {} * d_w.value
  FROM weights_now AS w, d_w
  WHERE iter < {} AND w.layer = d_w.layer AND w.input = d_w.input AND w.output = d_w.output
  )
)
SELECT max(precision) FROM (
    SELECT iter, COUNT(*)::float / (SELECT COUNT(DISTINCT sample_id) FROM one_hot) AS precision
    FROM (
       SELECT iter, pred.sample_id AS pred_sample, test.sample_id AS test_sample, pred.rank AS pred_rank, test.rank AS test_rank, pred.output = test.species_id AS proof
       FROM (
            SELECT *, RANK() OVER (PARTITION BY m.sample_id, iter ORDER BY value DESC) AS rank
            FROM (
              SELECT sample_id, output, 1 / (1 + exp(-1 * result)) AS value, iter
              FROM (SELECT m.sample_id, n.output, SUM(m.value * n.value) as result, m.iter
                     FROM (
                        SELECT sample_id, output, 1 / (1 + exp(-1 * result)) AS value, iter
                        FROM (SELECT m.sample_id, n.output, SUM(m.value * n.value) AS result, iter
                                FROM data AS m INNER JOIN weights_now AS n ON m.feature_id = n.input
                                WHERE n.layer = 0                                                  -- and n.iter=(select max(iter) from w)
                                GROUP BY m.sample_id, n.output, iter) calculation_3
                    ) AS m INNER JOIN weights_now AS n ON m.output = n.input
                     WHERE n.layer = 1 and n.iter = m.iter
                     GROUP BY m.sample_id, n.output, m.iter) calculation_4
            ) m ) pred,
            (SELECT *, RANK() OVER (PARTITION BY m.sample_id ORDER BY isValid DESC) AS rank FROM one_hot m) test) dummy
    WHERE pred_sample = test_sample AND pred_rank = 1 AND test_rank = 1
    GROUP BY iter, proof
    HAVING proof = true
    ORDER BY iter
) result;\n
'''
