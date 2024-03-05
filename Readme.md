# Model

## Modelo utilizado

Modelo Vector Generalizado

## Procesamiento de query

Explicación de manera general de cómo funciona este proceso:

1. **Tokenización:** Es el proceso de dividir el texto en palabras individuales o tokens. Esto es el primer paso en el análisis de texto y es crucial para entender la estructura del texto.

2. **Eliminación de ruido:** Este paso implica la eliminación de caracteres no deseados o irrelevantes del texto. Por ejemplo, convertir todas las palabras a minúsculas y eliminar las palabras que no son alfabéticas. Esto ayuda a normalizar el texto y a eliminar caracteres no deseados.

3. **Eliminación de palabras vacías (Stopwords):** Las palabras vacías son palabras comunes que no aportan significado al texto, como "the", "is", "at", etc. Se eliminan porque no contribuyen a la comprensión del contenido del texto.

4. **Reducción morfológica:** Este paso implica reducir las palabras a su forma base o raíz. Esto se hace mediante la lematización o el stemming. La lematización es más precisa ya que considera el contexto y la parte del discurso de la palabra, mientras que el stemming es más simple y puede no ser preciso en todos los casos.

5. **Procesamiento de la consulta:** Este es un paso que combina todos los anteriores en un solo proceso. Al llamar a este método, se realiza todo el preprocesamiento de la consulta en un solo paso, lo que facilita el análisis y la búsqueda de información en el texto.

En resumen, el proceso de preprocesamiento de texto es esencial para preparar el texto para su análisis. Al eliminar el ruido, las palabras vacías y reducir las palabras a su forma base, se facilita la comprensión del texto y se mejora la eficacia de este proyecto.

## Métricas utilizadas

Se calculan varias métricas de evaluación para medir la calidad de la recuperación de información . Estas métricas son importantes para entender cómo el sistema maneja los documentos relevantes e irrelevantes en relación con la consulta de búsqueda. 
A continuación se explica como se calcula estas:

1. **Bucle para calcular las métricas:** Se recorre la lista de `ranking`, que contiene los resultados de la búsqueda ordenados por su similitud con la consulta.

2. **Verificación de la relevancia del documento:** Para cada documento en el ranking, se verifica si su ID de documento (`doc_id`) está en la lista de documentos relevantes (`rels`) para la consulta actual. Si el ID del documento está en la lista de relevantes, se incrementa el contador `RR` (Relevants Recovered), lo que indica que un documento relevante fue recuperado correctamente. Si no está en la lista, se incrementa el contador `RI` (Recovered Irrelevant), lo que indica que un documento relevante no fue recuperado.

3. **Cálculo de los verdaderos negativos (NR):** Se calcula el número de verdaderos negativos (`NR`) restando el número de documentos relevantes recuperados (`RR`) del total de documentos relevantes para la consulta actual.

4. **Cálculo de los verdaderos negativos (NI):** Se calcula el número de verdaderos negativos (`NI`) restando el numero de documentos irrelevantes(total de documentos - documentos relevantes para la query) del  número de documentos recuperados irelevantes (`RI`) de la colección.

5. **Cálculo de la precisión (precision):** La precisión se calcula como la proporción de documentos relevantes recuperados (`RR`) en relación con la suma de documentos relevantes recuperados (`RR`) y documentos irrelevantes recuperados (`RI`).

6. **Cálculo del recall (recall):** El recall se calcula como la proporción de documentos relevantes recuperados (`RR`) en relación con la suma de documentos relevantes recuperados (`RR`) y documentos relevantes no recuperados (`NR`).

7. **Cálculo del F1-score (f1):** El F1-score es una medida que combina precisión y recall, y se calcula como el promedio armónico de la precisión y el recall.

8. **Cálculo del fallout (fallout):** El fallout se calcula como la proporción de documentos irrelevantes recuperados (`RI`) en relación con la suma de documentos irrelevantes recuperados (`RI`) y documentos irrelevantes no recuperados (`NI`).
