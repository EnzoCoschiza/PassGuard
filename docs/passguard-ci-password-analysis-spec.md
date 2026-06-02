# PassGuard CI - Especificacion Inicial SDD

## 1. Nombre de la feature

Password Security Analysis v1

## 2. Objetivo

Definir una feature inicial, simple y demostrable, que permita analizar una contrasena desde una interfaz web y devolver un resultado consistente, explicable y testeable. La feature debe servir como base para un workflow academico de CI/CD, calidad de software y despliegue, priorizando claridad funcional por sobre complejidad tecnica.

## 3. Alcance

Incluye en esta iteracion:

- Un frontend web con un campo para ingresar una contrasena y un boton para solicitar el analisis.
- Un backend FastAPI con los endpoints `GET /health` y `POST /password/analyze`.
- Un lexer que tokeniza la contrasena en grupos semanticos simples.
- Un analizador que aplica reglas funcionales y calcula score, nivel, advertencias y cumplimiento de reglas.
- Tests automatizados de backend para lexer, reglas y contrato HTTP.
- Estructura funcional apta para integrarse luego con CI/CD.

No incluye en esta iteracion autenticacion, persistencia, usuarios ni integraciones de infraestructura.

## 4. Historias de usuario

### HU-01 Analizar contrasena

Como usuario,
quiero ingresar una contrasena en la interfaz,
para obtener un analisis claro de su fortaleza.

### HU-02 Entender el resultado

Como usuario,
quiero ver score, nivel, advertencias, tokens y reglas cumplidas/incumplidas,
para entender por que una contrasena es segura o riesgosa.

### HU-03 Validar disponibilidad tecnica

Como desarrollador o integrador,
quiero disponer de un endpoint de salud,
para verificar rapidamente que el backend esta operativo en local y en CI/CD.

### HU-04 Verificar reglas automaticamente

Como equipo de desarrollo,
quiero reglas simples, deterministicas y testeables,
para automatizar validaciones en pipelines de calidad.

## 5. Reglas funcionales

### 5.1 Entradas

- El sistema debe aceptar una contrasena enviada como texto en formato JSON.
- La contrasena puede contener letras, numeros, simbolos y espacios.
- La contrasena no debe persistirse en base de datos ni registrarse en logs funcionales.

### 5.2 Endpoints

- `GET /health` debe responder exitosamente cuando la API este disponible.
- `POST /password/analyze` debe recibir una contrasena y devolver un analisis estructurado.

### 5.3 Tokenizacion

El lexer debe recorrer la contrasena de izquierda a derecha y agrupar caracteres contiguos del mismo tipo logico.

Tipos de token:

- `LOWERCASE_WORD`: secuencia contigua de letras minusculas ASCII `a-z`.
- `UPPERCASE_WORD`: secuencia contigua de letras mayusculas ASCII `A-Z`.
- `MIXED_WORD`: secuencia contigua de letras ASCII que mezcla mayusculas y minusculas dentro del mismo token.
- `NUMBER`: secuencia contigua de digitos `0-9`.
- `SYMBOL`: secuencia contigua de simbolos visibles que no son letras, digitos ni espacios.
- `WHITESPACE`: secuencia contigua de espacios o separadores en blanco.
- `UNKNOWN`: caracteres no clasificados por las categorias anteriores.

Reglas de agrupacion:

- Si una secuencia contiene solo letras minusculas, debe emitirse `LOWERCASE_WORD`.
- Si una secuencia contiene solo letras mayusculas, debe emitirse `UPPERCASE_WORD`.
- Si una secuencia alfabetica mezcla mayusculas y minusculas sin interrupcion, debe emitirse `MIXED_WORD`.
- Los espacios deben conservarse como token `WHITESPACE` para fines de trazabilidad del analisis.

### 5.4 Reglas de analisis obligatorias

El analizador debe evaluar como minimo:

- `MIN_LENGTH`: longitud total mayor o igual a 8.
- `HAS_LOWERCASE`: existe al menos una letra minuscula.
- `HAS_UPPERCASE`: existe al menos una letra mayuscula.
- `HAS_NUMBER`: existe al menos un digito.
- `HAS_SYMBOL`: existe al menos un simbolo visible no alfanumerico.
- `YEAR_NOT_DETECTED`: no existe una secuencia numerica que represente un ano entre 1900 y 2099.
- `NO_SIMPLE_SEQUENCE`: no existe alguna secuencia simple reconocible.
- `NO_EXCESSIVE_REPETITION`: no existe repeticion excesiva reconocible.

### 5.5 Detecciones de riesgo

#### Anos comunes

- Debe detectarse cualquier numero de cuatro digitos entre `1900` y `2099`.
- La deteccion aplica aunque el ano este incrustado dentro de la contrasena como token `NUMBER`.

#### Secuencias simples

Debe detectarse, al menos, la presencia de estas subsecuencias, sin importar si aparecen solas o embebidas:

- `123`
- `abc`
- `qwerty`

La deteccion debe ser case-insensitive para subsecuencias alfabeticas.

#### Repeticiones excesivas

Debe detectarse:

- tres o mas caracteres identicos consecutivos, por ejemplo `aaa`, `111`, `!!!`

### 5.6 Formula inicial de scoring

La formula debe ser lineal, facil de explicar y deterministica:

Puntaje base por reglas positivas:

- `MIN_LENGTH`: +25
- `HAS_LOWERCASE`: +15
- `HAS_UPPERCASE`: +15
- `HAS_NUMBER`: +15
- `HAS_SYMBOL`: +15

Bono de diversidad:

- +15 si cumple simultaneamente `HAS_LOWERCASE`, `HAS_UPPERCASE`, `HAS_NUMBER` y `HAS_SYMBOL`

Penalizaciones:

- `YEAR_DETECTED`: -30
- `SIMPLE_SEQUENCE_DETECTED`: -25
- `EXCESSIVE_REPETITION_DETECTED`: -25
- `WHITESPACE_DETECTED`: -10

Normalizacion:

- El score final debe truncarse al rango `0..100`.

### 5.7 Nivel de seguridad

El nivel debe calcularse despues del score final y con reglas de guardia:

- Si `MIN_LENGTH` falla, el nivel debe ser `weak`, sin importar el score numerico.
- Si el score final es `0..39`, el nivel debe ser `weak`.
- Si el score final es `40..74`, el nivel debe ser `medium`.
- Si el score final es `75..100`, el nivel debe ser `strong`.
- Si dos o mas advertencias de riesgo estan presentes, el nivel no debe superar `medium`, aunque el score numerico sea 75 o mas.

## 6. Reglas no funcionales

- La logica del analizador debe ser deterministica para la misma entrada.
- El backend debe responder JSON valido y tipado con Pydantic.
- El codigo debe organizarse para permitir tests unitarios y de API independientes.
- El analisis no debe depender de acceso a red, base de datos ni servicios externos.
- La implementacion inicial debe ser apta para ejecutarse localmente con `uv` y para correr tests con `pytest`.
- El frontend debe presentar el resultado sin recargar la pagina.
- La experiencia de uso debe ser simple y entendible en una demo academica.
- No deben exponerse trazas internas o stack traces en respuestas exitosas.

## 7. Criterios de aceptacion

### CA-01 Healthcheck

- Dado el backend en ejecucion
- Cuando un cliente invoca `GET /health`
- Entonces recibe `200 OK`
- Y una respuesta JSON que indique estado saludable

### CA-02 Analisis basico exitoso

- Dada una contrasena valida en formato JSON
- Cuando el cliente invoca `POST /password/analyze`
- Entonces recibe `200 OK`
- Y la respuesta incluye `score`, `level`, `tokens`, `warnings`, `passed_rules` y `failed_rules`

### CA-03 Password corta

- Dada una contrasena de menos de 8 caracteres
- Cuando se analiza
- Entonces `MIN_LENGTH` debe figurar en `failed_rules`
- Y `level` debe ser `weak`

### CA-04 Password intermedia

- Dada una contrasena que cumple longitud, minusculas, mayusculas y numeros pero no simbolos
- Cuando se analiza sin advertencias adicionales
- Entonces el nivel esperado debe ser `medium`

### CA-05 Password fuerte

- Dada una contrasena que cumple longitud, minusculas, mayusculas, numeros y simbolos
- Y no contiene ano, secuencias simples ni repeticiones excesivas
- Cuando se analiza
- Entonces el nivel esperado debe ser `strong`

### CA-06 Ano detectado

- Dada una contrasena que contiene un ano entre 1900 y 2099
- Cuando se analiza
- Entonces debe emitirse una advertencia `YEAR_DETECTED`
- Y `YEAR_NOT_DETECTED` debe aparecer en `failed_rules`

### CA-07 Secuencia simple detectada

- Dada una contrasena que contiene `123`, `abc` o `qwerty`
- Cuando se analiza
- Entonces debe emitirse una advertencia `SIMPLE_SEQUENCE_DETECTED`

### CA-08 Repeticion detectada

- Dada una contrasena con tres o mas caracteres identicos consecutivos
- Cuando se analiza
- Entonces debe emitirse una advertencia `EXCESSIVE_REPETITION_DETECTED`

## 8. Casos borde

- Contrasena vacia.
- Contrasena con solo espacios.
- Contrasena exactamente de 8 caracteres.
- Contrasena con caracteres repetidos no consecutivos, por ejemplo `ababab`, que no debe disparar repeticion excesiva.
- Contrasena con `2026` como parte de una secuencia numerica mas larga.
- Contrasena con mezcla de idiomas o caracteres Unicode.
- Contrasena con varios simbolos consecutivos.
- Contrasena con secuencias alfabeticas en mayusculas, por ejemplo `ABC`.
- Contrasena con `qWeRtY`, que debe detectarse como secuencia simple por comparacion case-insensitive.

## 9. Contratos esperados de API

### 9.1 `GET /health`

Respuesta `200 OK`:

```json
{
  "status": "ok",
  "service": "passguard-ci-api"
}
```

### 9.2 `POST /password/analyze`

Request:

```json
{
  "password": "UTN@2026segura"
}
```

Respuesta `200 OK`:

```json
{
  "score": 70,
  "level": "medium",
  "tokens": [
    { "type": "UPPERCASE_WORD", "value": "UTN" },
    { "type": "SYMBOL", "value": "@" },
    { "type": "NUMBER", "value": "2026" },
    { "type": "LOWERCASE_WORD", "value": "segura" }
  ],
  "warnings": [
    {
      "code": "YEAR_DETECTED",
      "message": "La contrasena contiene un ano reconocible."
    }
  ],
  "passed_rules": [
    "MIN_LENGTH",
    "HAS_LOWERCASE",
    "HAS_UPPERCASE",
    "HAS_NUMBER",
    "HAS_SYMBOL",
    "NO_SIMPLE_SEQUENCE",
    "NO_EXCESSIVE_REPETITION"
  ],
  "failed_rules": [
    "YEAR_NOT_DETECTED"
  ]
}
```

Notas del contrato:

- `score` debe ser entero.
- `level` debe ser uno de `weak`, `medium`, `strong`.
- `tokens` debe preservar el orden de aparicion original.
- `warnings` debe ser una lista vacia si no hay hallazgos.
- `passed_rules` y `failed_rules` no deben repetir claves.

Respuesta `422 Unprocessable Entity`:

- Si falta el campo `password`.
- Si `password` no es string.

## 10. Casos de prueba derivados de la especificacion

### 10.1 Tests unitarios del lexer

- Debe tokenizar `UTN@2026segura` en `UPPERCASE_WORD`, `SYMBOL`, `NUMBER`, `LOWERCASE_WORD`.
- Debe tokenizar `abcDEF` como `MIXED_WORD`.
- Debe tokenizar `   ` como un token `WHITESPACE`.
- Debe agrupar `!!!` como un token `SYMBOL`.

### 10.2 Tests unitarios del analizador

- Debe marcar `weak` si la contrasena tiene menos de 8 caracteres.
- Debe marcar `medium` para una contrasena que cumple longitud, mayusculas, minusculas y numeros, pero no simbolos.
- Debe marcar `strong` para una contrasena completa sin advertencias.
- Debe penalizar una contrasena con ano reconocido.
- Debe penalizar una contrasena con `123`.
- Debe penalizar una contrasena con `aaa`.
- Debe limitar el score a `0`.
- Debe limitar el score a `100`.
- Debe impedir `strong` si hay dos o mas advertencias.

### 10.3 Tests de API

- `GET /health` debe responder `200` y contrato esperado.
- `POST /password/analyze` debe responder `200` con estructura completa.
- `POST /password/analyze` sin `password` debe responder `422`.
- `POST /password/analyze` con `password` numerica debe responder `422`.

### 10.4 Tests de frontend

- Debe renderizar input y boton de analisis.
- Debe mostrar score y nivel luego de una respuesta exitosa.
- Debe mostrar advertencias y listas de reglas.
- Debe manejar estado de error si la API falla.

## 11. Fuera de alcance

- Base de datos.
- Registro o inicio de sesion real.
- JWT, OAuth o sesiones.
- Recuperacion de contrasena.
- Gestion de usuarios.
- Historial de analisis.
- Panel administrativo.
- Comparacion contra listas reales de contrasenas filtradas.
- Algoritmos avanzados de entropia o validacion criptografica.
- Integraciones reales con Docker, GitHub Actions, SonarQube, staging o notificaciones.

## 12. Riesgos o ambiguedades a aclarar antes de implementar

- Definir si el analizador debe considerar solo ASCII o soportar Unicode desde la primera iteracion.
- Confirmar si los espacios deben penalizarse siempre o si solo deben informarse como advertencia.
- Confirmar si una secuencia larga como `12345` dispara una sola advertencia por contener `123` o si debe tratarse como una categoria mas amplia.
- Definir si `MIXED_WORD` debe priorizarse siempre sobre separar cambios de mayuscula/minuscula dentro de una misma secuencia alfabetica.
- Confirmar si el frontend debe analizar solo bajo accion explicita del boton o tambien al presionar Enter.
- Acordar si los mensajes de advertencia deben quedar en espanol fijo o prepararse para futura internacionalizacion.
- Definir si el ejemplo academico requiere ocultar la contrasena en el input tipo password o mostrarla como texto para facilitar la demo.
- Confirmar si el score propuesto se considera estable para la demo o si el equipo quiere reservar margen para ajustarlo sin romper tests de contrato.

## Anexo A. Ejemplos de clasificacion esperada

### Ejemplo 1

Entrada:

```text
abc123
```

Resultado esperado:

- `level`: `weak`
- Falla `MIN_LENGTH`
- Detecta secuencia simple `abc`
- Detecta secuencia simple `123`

### Ejemplo 2

Entrada:

```text
Password2026
```

Resultado esperado:

- Cumple longitud, minusculas, mayusculas y numeros
- Falla `HAS_SYMBOL`
- Detecta `YEAR_DETECTED`
- Nivel esperado: `medium`

### Ejemplo 3

Entrada:

```text
UTN@2026segura
```

Resultado esperado:

- Tokens como en el ejemplo de contrato
- Detecta `YEAR_DETECTED`
- Sin secuencia simple ni repeticion excesiva
- Nivel esperado: `medium`
