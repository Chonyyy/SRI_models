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

1. **Presicion:** 
2. **Recall :** 
3. **F1:** 
4. **Fallout:** 
