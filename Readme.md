
# Autores

1. María de Lourdes Choy Fernández C412
2. Javier Rodríguez Sánchez C411
3. Jorge Alberto Aspiolea C412

## Modelo SRI implementado

Modelo Vector Generalizado.

## Consideraciones tomadas a la hora de desarrollar la solución

Consideramos tener en cuenta el contenido impartido en conferencias.

## Cómo ejecutar el proyecto

Bla bla

## Explicación de la solución desarrollada

### Colecciones

Las colecciones de documentos de prueba que se usan en el sistema para realizar consultas sobre ellas es la popular colección de Cranfield.

### Procesamiento de query (Class `Query`)

Explicación de manera general de cómo funciona este proceso:

1. **Tokenización:** Es el proceso de dividir el texto en palabras individuales o tokens. Esto es el primer paso en el análisis de texto y es crucial para entender la estructura del texto.

2. **Eliminación de ruido:** Este paso implica la eliminación de caracteres no deseados o irrelevantes del texto. Por ejemplo, convertir todas las palabras a minúsculas y eliminar las palabras que no son alfabéticas. Esto ayuda a normalizar el texto y a eliminar caracteres no deseados.

3. **Eliminación de palabras vacías (Stopwords):** Las palabras vacías son palabras comunes que no aportan significado al texto, como "the", "is", "at", etc. Se eliminan porque no contribuyen a la comprensión del contenido del texto.

4. **Reducción morfológica:** Este paso implica reducir las palabras a su forma base o raíz. Esto se hace mediante la lematización o el stemming. La lematización es más precisa ya que considera el contexto y la parte del discurso de la palabra, mientras que el stemming es más simple y puede no ser preciso en todos los casos.

5. **Procesamiento de la consulta:** Este es un paso que combina todos los anteriores en un solo proceso. Al llamar a este método, se realiza todo el preprocesamiento de la consulta en un solo paso, lo que facilita el análisis y la búsqueda de información en el texto.

En resumen, el proceso de preprocesamiento de texto es esencial para preparar el texto para su análisis. Al eliminar el ruido, las palabras vacías y reducir las palabras a su forma base, se facilita la comprensión del texto y se mejora la eficacia de este proyecto.

### Class `TextProcessor`

El objetivo principal de esta clase es preparar los documentos y las consultas para su análisis en el sistema de recuperación de información, utilizando técnicas de preprocesamiento de texto y representación vectorial. Esto incluye la tokenización, la eliminación de ruido y palabras vacías, la lematización o el stemming, el filtrado de palabras por frecuencia, y la representación de los documentos como vectores utilizando el modelo BoW o TF-IDF. Además, la clase proporciona métodos para calcular la similitud entre la consulta y los documentos, guardar consultas y proporcionar recomendaciones basadas en la retroalimentación del usuario.

Aquí está un desglose de lo que hace cada parte del código:

1. **Inicialización (`__init__`):**
   - Carga un conjunto de datos llamado "cranfield" utilizando la biblioteca `ir_datasets`.
   - Elimina dos documentos específicos del conjunto de datos (índices 470 y 993).
   - Tokeniza, elimina ruido, elimina palabras vacías y realiza una reducción morfológica en los documentos.
   - Filtra los tokens por su frecuencia de ocurrencia para crear un diccionario y un corpus.
   - Representa los documentos como vectores utilizando el modelo Bag of Words (BoW) o TF-IDF.
   - Generaliza los vectores utilizando un método específico para el modelo vectorial generalizado.

2. **Tokenización (`tokenization_nltk`):**
   - Utiliza la biblioteca NLTK para tokenizar los documentos en palabras individuales.
   - Intenta crear un archivo `feedback.json` para almacenar retroalimentación de los usuarios, pero si ya existe, carga los datos existentes.

3. **Eliminación de ruido (`remove_noise_nltk`):**
   - Convierte todas las palabras a minúsculas y elimina las palabras que no son alfabéticas.

4. **Eliminación de palabras vacías (`remove_stopwords`):**
   - Elimina las palabras vacías del conjunto de palabras en inglés utilizando NLTK.

5. **Reducción morfológica (`morphological_reduction_nltk`):**
   - Realiza la lematización o el stemming en las palabras tokenizadas, dependiendo de si se utiliza la lematización o no.

6. **Filtrado de tokens (`filter_tokens_by_occurrence`):**
   - Crea un diccionario de palabras utilizando Gensim y filtra las palabras que aparecen con demasiada frecuencia o muy poco.

7. **Representación vectorial (`vector_representation`):**
   - Representa los documentos como vectores utilizando el modelo BoW o TF-IDF.

8. **Generación de vectores independientes (`generate_independents_vectors`):**
   - Genera una lista de vectores independientes que se utilizarán para la generalización.

9. **Generalización (`generalize`):**
   - Realiza una generalización de los vectores de los documentos o de la consulta utilizando un método específico para el modelo vectorial generalizado.

10. **Procesamiento de consultas (`query_processor`):**
    - Procesa una consulta dada, la convierte en un vector utilizando el mismo método que los documentos.
    - Guarda la consulta y la procesa para su posterior uso.

11. **Similitud (`similarity`):**
    - Calcula la similitud entre la consulta y los documentos utilizando un índice de similitud de Gensim.

12. **Retroalimentación (`feedback`):**
    - Permite al usuario proporcionar retroalimentación sobre un documento específico.

13. **Guardar (`save`):**
    - Guarda la consulta actual en un archivo `recomendation.json`.

14. **Recomendar (`recomend`):**
    - Carga una consulta previa desde `recomendation.json`, procesa la consulta y devuelve los documentos más similares.

Se utilizan varias bibliotecas externas, como `ir_datasets` para cargar conjuntos de datos, `nltk` para el procesamiento de texto, `gensim` para la representación vectorial y la similitud, y `numpy` y `math` para cálculos matemáticos. También utiliza la clase `Query` definida en otro módulo para procesar las consultas.

### Métricas utilizadas

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

## Insuficiencias de la solución y mejoras propuestas.

----------------------------------------------------------------------------

