STATEMENT_1 = '''
SELECT matrixa.rowIndex AS rowIndex, {}(matrixa.val * matrixb.val * vectorv.val) AS val
FROM matrixa, matrixb, vectorv
WHERE matrixa.columnIndex = matrixb.columnIndex AND matrixb.rowIndex = vectorv.rowIndex
GROUP BY matrixa.rowIndex;'''

STATEMENT_2 = '''
SELECT matrixa.rowIndex AS rowIndex, (matrixa.val * matrixb.val * vectorv.val) AS val
FROM matrixa, matrixb, vectorv
WHERE matrixa.columnIndex = matrixb.columnIndex AND matrixb.rowIndex = vectorv.rowIndex;'''

STATEMENT_3 = '''
WITH result(rowIndex, val) AS (
    SELECT matrixb.columnIndex, {}(vectorv.val * matrixb.val) AS val
    FROM vectorv, matrixb
    WHERE vectorv.rowIndex = matrixb.rowIndex
    GROUP BY matrixb.columnIndex
) SELECT * FROM result ORDER BY rowIndex;'''

STATEMENT_4 = '''
WITH result(rowIndex, val) AS (
    SELECT matrixb.columnIndex, {}(vectorv.val * matrixb.val) AS val
    FROM vectorv, matrixb
    WHERE vectorv.rowIndex = matrixb.rowIndex
    GROUP BY matrixb.columnIndex
) SELECT matrixa.rowIndex AS rowIndex, {}(result.val * matrixa.val) AS val
  FROM result, matrixa WHERE result.rowIndex = matrixa.columnIndex 
  GROUP BY matrixa.rowIndex;'''