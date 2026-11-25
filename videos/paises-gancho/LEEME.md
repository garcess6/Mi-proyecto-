# Vídeos por país con gancho y presentador

Los proyectos base (`pais-cod`, `pais-eth`, `pais-nga`) están en la rama `claude/sleepy-ramanujan-q0w249`.

- `hooks.json`: frase del gancho de cada país e idioma.
- `hookify.py <cod|eth|nga>`: crea `gen_hook.py` dentro del proyecto del país. Ese script añade el gancho como primera escena, el presentador que habla y señala, y el dedo. Genera las carpetas `hook-<idioma>-<formato>`.
- La voz del gancho está en `assets/vo_<idioma>/h0.wav` de cada país; aquí van copiadas en `vo/`.

| País | Gancho |
|---|---|
| RD Congo (EN) | Over thirteen hundred deaths in just seven months. That's what cholera did in the Congo in 2025. And it starts with the water people drink. |
| RD Congo (FR) | Plus de mille trois cents morts en seulement sept mois. Voilà ce que le choléra a fait au Congo en 2025. Et tout commence par l'eau que l'on boit. |
| Etiopía | Over twenty-seven thousand cholera cases in a single year. In Ethiopia, the outbreak has lasted since 2023. And it starts with the water people drink. |
| Nigeria | In 2024, three in every hundred people who caught cholera in Nigeria died. And it often starts with water that looks perfectly clean. |

Los datos del gancho son los mismos que ya aparecían (con su fuente) dentro de cada vídeo.
