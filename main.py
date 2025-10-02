```python
import feedparser
import requests
import os

URL del feed del DOF
DOF_RSS_URL = "https://www.dof.gob.mx/rss.php"

Palabras clave de interés
KEYWORDS = ["penal", "proceso penal", "constitución", "constitucional", "reforma", "código penal", "derechos humanos"]

Leer el RSS
feed = feedparser.parse(DOF_RSS_URL)

Filtrar entradas relevantes
entradas_relevantes = [
    entry for entry in feed.entries
    if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.summary.lower() for keyword in KEYWORDS)
]

Si hay algo relevante, enviar a OpenAI
if entradas_relevantes:
    prompt_base = """
Eres un Asistente Jurídico Profesional Automatizado para la Lic. Ma. Rosa Correa Martínez.
Tu única función es entregar con fidelidad y exactitud las reformas, adiciones o derogaciones publicadas en el DOF
relacionadas con Derecho Penal Procesal y Derecho Constitucional.

Por cada artículo, responde únicamente con:
1. Número y título del artículo reformado – adicionado - derogado
2. Texto completo del artículo conforme al DOF
3. Fecha de publicación y/o entrada en vigor (si aplica)
4. Fuente (https://www.dof.gob.mx/rss.php)
5. No expliques, no resumas, no interpretes. Sólo entrega el texto legal íntegro.

Contenido:
"""

    for entry in entradas_relevantes:
        content = f"{entry.title}entry.linkentry.summary"
        full_prompt = prompt_base + content

        # Enviar a OpenAI
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": full_prompt}],
                "temperature": 0
            }
        )

        result = response.json()
        print(result['choices'][0]['message']['content'])

else:
    print("No se encontraron reformas relevantes hoy.")
```

