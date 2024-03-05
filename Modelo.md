
# Abstract

En los sistemas de recuperación de información siempre se busca extraer información de interés de algún sistema de recursos que normalmente son documentos. Para esto se han creado con el paso del tiempo varios modelos matematicos que permiten cumplir el objetivo. Entre estos modelos están los clásicos que son el Modelo Booleano, Vectorial, Probabilístico. La desventaja principal que suelen tener los modelos anteriores es que asumen la independencia de los términos y por esta razón se comenzaron a crear otros que solventaran este problema y uno de ellos es el Modelo Vectorial Generalizado que es el que se desarrollará en este seminario.

# Introducción

El modelo vectorial generalizado fue propuesto en 1985 por Wong para solventar uno de los problemas del modelo vectorial clásico, que es, asumir que todos los términos indexados son independientes. La propuesta era una interpretación en la cual los términos indexados eran asumidos linealmente independientes pero no ortogonales por pareja, o en otras palabras para evaluar relaciones entre términos. En el modelo vectorial generalizado dos vectores de términos indexados no tienen porque ser vectores ortogonales. Esto quiere decir que los vectores de términos indexados no son vistos como los vectores ortogonales que componen la base del sistema. De hecho estos son compuestos por componentes mas pequeños que vienen siendo los minterms.

# Explicación del Framework

La base teórica de este modelo, además de los espacios n-dimensionales y las operaciones entre vectores del álgebra lineal, está compuesta también por un algebra booleana libre B compuesta generada por n literales además de una interpretación vectorial de la relación entre términos. Dado que solo las últimas dos partes de este framework no han sido trabajadas en la carrera vamos a ahondar solamente en estas siguiendo las explicaciones que se encuentran en el articulo "Generalized Vector Space Model in Information Retrieval" de S. K. M. Wong, Wojciech Ziarko y Patrick C. N. Wong. Un producto fundamental de n literales es una conjunción en la que cada literal t aparece exactamente una única vez ya sea complementado o sin complementar. Los 2 productos fundamentales en n literales son join-irreducibles. Esto quiere decir que no hay un producto fundamental que pueda ser escrito como una conjunción de otros dos productos fundamentales.

# Representación de Documentos y Consultas

En este modelo se utilizan las mismas representaciones para los documentos y las consultas que en el modelo vectorial clásico, con la única diferencia de que a la hora de representar el vector de un documento a este se le multiplica el peso (weigth) de cada termino por un un factor k de correlación (que explicamos mas adelante en el documento). Lo mismo se hace con el vector de las consultas.

# Definición Formal del Modelo

La definición formal dada en el libro Modern Information Retrieval en la pagina 41 es la siguiente:

# Mimterm Activo

Un mimterm se dice activo si existe algún documento que tenga el patron de ocurrencia de términos que describe el mismo. Es decir, si no existe un documento que tenga solamente los 2 primeros términos indexados del sistema, entonces el mimterm m = (1, 1, 0, … , 0) asociado con este patron no se encontraría activo.

# Cálculo del Ranking

Para el modelo en cuestión se usa la misma función de ranking que para el modelo vectorial usual:

# Ejemplo de Calculo de k

Supongamos que tenemos un sistema con 12 documentos y 4 términos tal que:
D1 = (2, 1, 0, 0);  
D2 = (5, 1, 0, 0);  
D3 = (1, 1, 1, 1);  
D4 = (0, 0, 2, 2);  
D5 = (0, 1, 1, 2);  
D6 = (0, 0, 1, 1);  
D7 = (0, 0, 1, 0);  
D8 = (1, 1, 0, 0);  
D9 = (2, 1, 1, 1);  
D10 = (0, 2, 2, 2);  
D11 = (1, 0, 2, 0);  
D12 = (0, 0, 2, 1)

Utilizamos 6 minterms como vectores independientes para formar una base:  
M 1 = (1, 1, 0, 0);  
M 2 = (1, 1, 1, 1);  
M 3 = (0, 0, 1, 1);  
M 4 = (0, 1, 1, 1);  
M 5 = (0, 0, 1, 0);  
M 6 = (1, 0, 1, 0)  

Sean los vectores independientes:  
V 1 = (1, 0, 0, 0, 0, 0, 0);  
V 2 = (0, 1, 0, 0, 0, 0, 0);  
V 3 = (0, 0, 1, 0, 0, 0, 0);  
V 4 = (0, 0, 0, 1, 0, 0, 0);  
V 5 = (0, 0, 0, 0, 1, 0, 0);  
V 6 = (0, 0, 0, 0, 0, 1, 0)  

Tal que V representa al minterm M , cada par V , V es ortogonal (i ≠ j). Los cuatro términos k , k , k , k y k son representados por una combinación de los vectores independientes:

# Ventajas y Desventajas

Este modelo extiende las funcionalidades del modelo vectorial tradicional, modelando además la correlación entre términos y documentos, lo que permite obtener mejores resultados de búsqueda en algún casos, aunque no está claro en que casos las relaciones término a término mejoran la recuperación de documentos. Sin embargo, el modelo es más complejo y requiere más recursos computacionales para su cálculo. Además, el modelo no es escalable, ya que el número de términos y documentos crece exponencialmente con el tamaño del vocabulario. Por último, el modelo no es capaz de modelar la correlación entre términos que no estén indexados.

# Comparación del modelo en cuestión con otros modelos estudiados

Tal como sucede con el modelo vectorial clásico este se diferencia del modelo booleano en que no solamente modela la existencia de términos en los documentos, si no que además modela la frecuencia de los mismos. Además este es mas complejo que el vectorial, ya que simula la relación entre términos, cosa que también vemos en el modelo fuzzy pero en el caso en cuestión también se tiene en cuenta la frecuencia en que términos distintos se encuentran en el mismo documento.

# Conclusiones

En la práctica el Modelo Vectorial es de los más sencillos de implementar y ha resultado ser de bastante valor en los Sistemas de Recuperación de Información. Pero como se ha expuesto en este trabajo su mayor desventaja radica en asumir que los términos son independientes y por ende no permite aprovechar la crucial ventaja de tener alguna forma de correlacionar los términos. Es por esto que se crea el Modelo Vectorial Generalizado y aquí en este documento se ha visto como de una forma sencilla se pueden relacionar los vectores de términos indexados a un espacio vectorial 2 -dimensional usando algebra de bool con los minterms.