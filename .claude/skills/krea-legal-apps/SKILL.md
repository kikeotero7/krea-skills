---
name: krea-legal-apps
description: Usar al crear, revisar o publicar cualquier app o web de KREAVANCE, y antes de cada publicación. Protocolo legal según la ley española y europea: aviso legal, privacidad, condiciones, cookies, desistimiento, información sobre la IA, consentimientos separados y registro trazable.
---

# Protocolo legal de KREAVANCE para apps y webs

Referencia completa: «Checklist legal de KREAVANCE para apps y webs» (Claude Docs, https://claude.ai/artifact/Eef4fLsTQdnnGJsRF9jhFj). Esta skill es su versión de trabajo. **No sustituye a un abogado.**

## 1. Antes de empezar (apuntarlo en el CLAUDE.md del repo)

Responder y dejar escrito, en una sección «Legal»:
- Qué datos recoge y para qué.
- Si hay datos sensibles: salud, menores, ubicación, fotos o vídeos de personas.
- A quién vende: particulares o empresas, y en qué países.
- Si cobra: pago único o suscripción; cómo son las devoluciones.
- Qué promete al cliente (plazos, resultados, disponibilidad).
- Qué proveedores tocan los datos (hosting, correo, IA, pagos, analítica) y en qué país están.
- Si hay cookies que no sean técnicas.
- Quién es el titular: KREAVANCE o el cliente (si es el cliente, sus datos van en los documentos, nunca en el repo si son personales).

## 2. Documentos obligatorios

Enlazados en la pantalla de entrada y en el pie de todas las páginas:

| Documento | Cuándo | Norma |
|---|---|---|
| Aviso legal (titular, NIF, dirección, correo) | Siempre | LSSI art. 10 |
| Política de privacidad | Siempre que haya datos personales | RGPD arts. 13-14 y LOPDGDD |
| Condiciones de uso o de contratación | Siempre; de contratación si se vende | LGDCU y LSSI |
| Política de cookies | Si hay cookies no técnicas (si solo hay técnicas, decirlo) | LSSI art. 22.2 y guía de la AEPD |
| Desistimiento y reembolsos | Si se vende a particulares: 14 días naturales; la renuncia en contenido digital, con casilla propia | LGDCU arts. 102-108 |
| Información sobre la IA | Si la app o la web usa IA que habla con personas o genera contenido | Reglamento de IA, art. 50 |

Cada documento lleva **versión y fecha**. Si cambia algo importante, se pide nueva aceptación.

## 3. En la app o la web

- **Casillas separadas y sin marcar**: condiciones / privacidad / datos sensibles / comunicaciones comerciales. Nunca «acepto todo».
- **Registro trazable** de cada aceptación y retirada: quién, qué documento, qué versión, fecha y hora. La IP solo si hace falta, y diciéndolo en la privacidad.
- **Cookies**: solo técnicas, o un aviso con «Aceptar» y «Rechazar» igual de visibles y nada cargado antes de aceptar.
- **Minimización**: pedir solo los datos necesarios.
- **Derechos desde la app**: descargar mis datos, corregir, borrar la cuenta y retirar consentimientos.
- **Proveedores**: contrato de encargado del tratamiento y datos en la UE (o garantías si salen).
- **Contenido con licencia**: imágenes, vídeos, música y fuentes propias o con licencia; apuntar el origen en el repo.
- **IA declarada**: avisar de que se habla con una IA y marcar el contenido generado.
- **Edad mínima**: indicarla; con menores, consentimiento del tutor.
- **Accesibilidad**: Ley 11/2023 (contraste, teclado, textos alternativos).
- **Seguridad**: pasar la skill `krea-auditoria-seguridad` antes de publicar.
- **Registro de actividades de tratamiento** y **EIPD** (evaluación de impacto) si hay datos de salud, menores o tratamiento a gran escala.

## 4. Antes de cada publicación

Repasar las secciones 2 y 3 y anotar en el CLAUDE.md qué está hecho y qué falta. Si falta algo obligatorio, avisar a Kike antes de publicar.

## 5. Abogado

Antes del primer cliente de pago, revisar con un abogado: condiciones de contratación y desistimiento, la privacidad si hay datos de salud o de menores, la EIPD y los contratos con los proveedores.

## Forma de trabajar

- Se aplica app por app, en el hilo de cada proyecto. No tocar repos de clientes desde otro hilo.
- Textos legales en español claro, sin tecnicismos innecesarios.
- Datos personales de clientes o usuarios nunca en el repo.
