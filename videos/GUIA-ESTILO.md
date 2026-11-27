# Guía de estilo de los vídeos AquaCore

## Reglas nuevas (desde el 24/11/2026)
1. **Empezar con el gancho.** Los primeros 2-5 segundos llevan lo más impactante del vídeo: el dato que más sorprende, la consecuencia más grave o la pregunta más directa. Primero el impacto y después el contexto.
   - Ejemplo del cólera: *"It can kill within hours. And in 2026, it's still here. This is cholera."* (reloj que gira rápido + "WITHIN HOURS").
   - El tema o título del vídeo se dice al final del gancho, no al principio.
   - En el segundo 0 ya tiene que haber movimiento en pantalla (algo que aparece o se mueve), nunca una pantalla quieta.
2. **Presentador guía.** En todas las escenas sale el muñeco gota de AquaCore (pequeño, en un lateral) que:
   - **habla**: abre la boca con cada palabra de la voz;
   - **señala**: levanta el brazo hacia lo que se está explicando;
   - **reacciona**: cambia de cara según el tono (preocupado, pensativo, contento).
3. **Dedo que señala.** Una mano con el índice estirado va hasta cada elemento clave justo cuando la voz lo nombra y le da un "toque". Desaparece en cada cambio de escena y en la tarjeta final.
4. En la tarjeta final el presentador **saluda con la mano**.

## Reglas que se mantienen
- Voz "Heart" (Kokoro af_heart) en inglés, subtítulos palabra a palabra, palabras clave en azul.
- Muñeco de palitos, fondo blanco, azul #1E7FD8, logo solo al final.
- Formatos: 9:16 (Reels/Stories) y 16:9 (YouTube/LinkedIn).
- Sin cifras inventadas: cada dato con su fuente (en pantalla, en el texto, o en ambos).
- Sin "elimina todo" ni "100 % seguro". Sin comparativas con marcas.
- Tarjeta final con una pregunta para los comentarios. Al final del vídeo, pedir que se comparta o se guarde.

## Dónde está el código
- `videos/wn-colera/index.html`: primer vídeo con el gancho y el presentador. Las funciones `gAt` (colocar), `gPoint` (señalar) y `gTalk` (hablar) del bloque "GUIDE" se pueden copiar a cualquier episodio.

## Formato "Reality Check" (vídeos que rebaten un clip ajeno)
Basado en las referencias de @eldatomanda. Versión dinámica en `videos/reality-raw-water/build2.py`.
1. **0-3 s:** el clip a pantalla completa con su frase y un sello rojo con la pregunta ("LIVE LONGER?").
2. **El clip se encoge** en una tarjeta inclinada; el título va cambiando arriba (palabra clave en un recuadro azul) y salen pegatinas con datos (likes, guardados, cita).
3. **Pantalla de marca** (rayos que giran + "REALITY CHECK") justo antes de empezar a rebatir.
4. **Secciones numeradas** ("1 · …"): su clip entra volando, su frase en una tarjeta de cita, nuestros datos como pegatinas una a una y un **veredicto** de color (✗ rojo, ⚖ naranja, ↻ azul) con la fuente.
5. **Marcador final** con todas las afirmaciones y su veredicto, y la conclusión ("TESTED ✓ TREATED ✓").
6. Fondo cuadriculado azul claro, ritmo de un cambio en pantalla cada ~1 s, presentador gota señalando.
   **Sonido:** clic en cada toque del dedo, whoosh en entradas y salidas, pop en pegatinas, golpe en sellos y veredictos, ding en la pantalla de marca y el final (efectos propios en `videos/reality-raw-water/sfx/`).
7. Clip ajeno: máx. 10-20 s, sin su audio, crédito siempre visible. En TikTok, mejor con "Stitch".
