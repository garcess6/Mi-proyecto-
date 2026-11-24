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
