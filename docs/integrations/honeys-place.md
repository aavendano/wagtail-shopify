# Honey's Place — respaldo técnico y funcional
Fecha: 2026-11-18. Estado: archivo histórico, no certificación de implementación.

## Fuentes y alcance
- Honeys_API_Docs.pdf, documentación del proveedor (secciones 1–8).
- honeys_place_api_instructions.md, extracción histórica (secciones 1–10).
- Conversaciones del proyecto Honey's Place Integration del 5 y 6 de diciembre de 2025.
- Contexto posterior de arquitectura de PlayLoveToys: Shopify como backend comercial y Django para integraciones. Mercado inicial USA; Canadá separado. Evaluaciones históricas de Saleor y otras plataformas no constituyen decisión de migración.
No se incluyen credenciales, URLs privadas de feeds ni datos personales. No se han ejecutado llamadas reales.

## API y autenticación
Endpoint: https://www.honeysplace.com/ws/
XML, Content-Type: application/xml. Cuenta y token (password) dentro de HPEnvelope. Obtenerlos en My Account → Data Integration → API Setup (la extracción también menciona Order API para actualización de token). Actualizar endpoint y contraseña al migrar desde la API antigua.

| Operación | Método | Elemento |
|---|---|---|
| Enviar pedido | POST | order |
| Consultar estado | GET | orderstatus |
| Consultar stock | GET | stockcheck |

El PDF especifica XML raw en el cuerpo incluso para GET. La extracción histórica menciona form-data o parámetro xmldata. Confirmar formatos soportados con proveedor; evitar enviar secretos en URL. Respuestas XML. Codificación de ejemplos ISO-8859-1 salvo solicitud stock UTF-8. Respetar declaración y bytes reales.

## Catálogo y feeds
El catálogo no se descarga mediante la API de pedidos. My Account → Data Integration → Data Feeds → crear/editar → filtrar por categoría y fabricante → guardar → descargar mediante URL correspondiente. La generación puede tardar.
Formatos: XML, CSV, JSON, WooCommerce, Shopify.
La extracción indica precios, MAP y metadata adicional; imágenes de feeds modernos: anteponer https://www.honeysplace.com a rutas relativas. Verificar esquema real y disponibilidad de peso/dimensiones.
Feeds legacy (históricos, HTTP, disponibilidad no verificada):
- http://ws.honeysplace.com/ws/xml/honeysinventoryv2_0.xml
- http://ws.honeysplace.com/ws/xml/honeysinventory_v_1.0.txt
El segundo es delimitado por tabuladores, no CSV automático. Descarga diaria según extracción.
Imágenes legacy: http://ws.honeysplace.com/pics/{filename} si solo hay nombre; http://ws.honeysplace.com/{path}/{filename} si incluye ruta.

## Integración nativa Shopify según PDF
1. Products → Import → seleccionar CSV Shopify → Upload and Preview → revisar muestra y cantidad → Import Products. Ajustar campos conforme a https://help.shopify.com/en/manual/products/import-export/using-csv.
2. Products → seleccionar productos → Bulk Edit → Columns → Track Quantity → habilitar y guardar.
3. Honey's Place → My Account → Data Integration → Shopify → editar cuenta.
4. Enabled, Site Name, Admin API Access Token, API Key, API Secret Key, Admin URL.
5. El PDF describe creación de app en Shopify Apps → App and sales channel settings → Develop apps → Create app → Configuration → Admin API Integration → Configure → permisos → API Credentials → Install app → obtener token. Admin URL desde Settings → Domains.
6. Guardar credenciales → Sync Products → esperar aparición de productos → Product → Sync para actualizar stock.
Este procedimiento es histórico; verificar cambios actuales de Shopify y permisos mínimos. No compartir token general si puede usarse uno dedicado.

## Envío de pedidos
POST al endpoint común. Ejemplo normalizado (el PDF contiene una errata en la etiqueta reference).
```xml
<?xml version="1.0" encoding="iso-8859-1"?>
<HPEnvelope>
  <account>ACCOUNT_PLACEHOLDER</account>
  <password>TOKEN_PLACEHOLDER</password>
  <order>
    <reference>TESTOrder123</reference>
    <shipby>RTSHOP</shipby>
    <date>05/16/11</date>
    <items><item><sku>CC-USCCYM</sku><qty>1</qty></item></items>
    <last>CustomerLast</last><first>CustomerFirst</first>
    <address1>Address1</address1><address2>Address2</address2>
    <city>City</city><state>NY</state><zip>12345</zip><country>US</country>
    <phone>Phone</phone><emailaddress>Email</emailaddress>
    <instructions>Special instructions</instructions>
  </order>
</HPEnvelope>
```
Fecha MM/DD/YY. Respuesta:
```xml
<HPEnvelope><reference>TESTOrder123</reference><code>100</code></HPEnvelope>
```
Referencias que comienzan con TEST (sin distinguir mayúsculas) no se procesan realmente: se marcan enviadas con tracking ficticio 123456789. El ejemplo de estado del PDF usa 0123456789; preservar diferencia y no asumir igualdad literal.

## Estado de pedido
GET:
```xml
<HPEnvelope><account>ACCOUNT_PLACEHOLDER</account><password>TOKEN_PLACEHOLDER</password><orderstatus>TESTOrder123</orderstatus></HPEnvelope>
```
Respuesta ejemplo del PDF:
```xml
<HPEnvelope>
<reference>TESTOrder123</reference><salesorder>SO-000000</salesorder>
<orderdate>2017-02-01 19:16:32</orderdate><shipagent>USPS</shipagent>
<shipservice>FIRST</shipservice><freightcost>2.65</freightcost>
<trackingnumber1>0123456789</trackingnumber1><status>Shipped</status>
</HPEnvelope>
```
La extracción incluye salesinvoice y la respuesta no enviada:
```xml
<HPEnvelope><reference>YourOrderNumber</reference><orderdate>Date</orderdate><cancelled>Yes/No</cancelled><status>Not Yet Shipped</status></HPEnvelope>
```
Campos opcionales y estados completos por validar. freightcost es costo posterior al pedido, no cotización previa documentada.

## Stock
GET:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<HPEnvelope><account>ACCOUNT_PLACEHOLDER</account><password>TOKEN_PLACEHOLDER</password>
<stockcheck><sku>CC-USCCYM</sku></stockcheck></HPEnvelope>
```
```xml
<HPEnvelope><stock><item><sku>CC-USCCYM</sku><qty>16</qty></item></stock></HPEnvelope>
```
Extracción histórica: múltiples elementos sku y máximo 25 por solicitud (no explicitado en PDF). Confirmar mediante prueba.

## Appendix A — transporte
| Carrier | Service | Texto antiguo | Código |
|---|---|---|---|
| FedEx | First Overnight | first overnight | F001 |
| FedEx | Priority Overnight | priority | F002 |
| FedEx | Standard Overnight | standard overnight | F003 |
| FedEx | 2 Day Air | 2day | F004 |
| FedEx | Express Saver | express saver | F005 |
| FedEx | Ground USA/Canada/Mexico | ground service | F006 |
| FedEx | Ground Home Delivery | home delivery | F007 |
| FedEx | International Priority | priority intl | F008 |
| FedEx | International Economy | economy intl | F009 |
| FedEx | SmartPost | smartpost | F010 |
| USPS | Express Mail Overnight | express | P001 |
| USPS | Priority Mail | priority | P002 |
| USPS | First Class (<13oz) | first | P003 |
| USPS | International Express | express intl | P005 |
| USPS | International Priority | priority intl | P006 |
| USPS | International First | first intl | P007 |
| USPS | Priority Flat Rate | priority/flat rate | P008 |
| UPS | Next Day Air | next day air | U001 |
| UPS | 2nd Day Air | 2nd day air | U002 |
| UPS | 3 Day Select | 3 day select | U003 |
| UPS | Ground | ground | U004 |
| UPS | Standard Canada | standard | U005 |
| Honeys | Customer Pickup | pickup | PICKUP |
| Cheapest | Best Rate | rateshop | RTSHOP |

Nombres históricos, no confirmar vigencia actual por inferencia.

## Appendix B — errores
| Código | Significado | Fuente |
|---|---|---|
| 100 | Pedido aceptado para procesamiento | Ambas |
| 999 | Usuario/contraseña inválidos | Ambas |
| 800 | Nombre requerido | Ambas |
| 801 | Apellido requerido | Extracción |
| 802 | Address1 requerido | Extracción |
| 803 | Ciudad requerida | Extracción |
| 804 | Estado requerido | Ambas |
| 805 | ZIP requerido | Extracción |
| 806 | ZIP inválido | Extracción |
| 807 | País inválido | Extracción |
| 808 | Email inválido | Extracción |
| 809 | Estado debe tener dos caracteres | Extracción |
| 700 | Referencia ya utilizada | Ambas |
| 701 | Referencia requerida | Extracción |
| 600 | Código de envío inválido | Ambas |
| 500 | Uno o más productos descontinuados | Ambas |
| 501 | Uno o más productos inexistentes | Ambas |
| 400 | Producto duplicado en pedido | Ambas |
| 300 | Consulta de pedido aún no enviado al proveedor | Ambas |
| 0 | Error desconocido, contactar soporte | Ambas |

## cURL
Ejemplo raw conforme al PDF:
```sh
curl -X POST 'https://www.honeysplace.com/ws/' -H 'Content-Type: application/xml' --data-binary @order.xml
```
Ejemplo histórico de extracción:
```sh
curl -X POST 'https://www.honeysplace.com/ws/' -d "xmldata=$(cat order.xml)"
```
No usar secretos reales en archivos versionados. La segunda variante debe validarse; el ejemplo original no garantiza URL encoding correcto.

## Alcance funcional histórico
1. Importar productos.
2. Actualizar precios e inventario; Honey's Place puede seguir actualizando inventario inicialmente.
3. Pre-order: estimar shipping antes de enviar pedido, porque no hay costo fijo y depende de peso y volumen. Pre-order aquí significa validación/cálculo previo a compra al proveedor, no necesariamente venta de productos futuros.
4. Procesar pedido.
Mercado estadounidense como primera implementación. Evaluación histórica de arquitectura alternativa debido a carga de trabajo y transición .ca → .com.

## Arquitectura propuesta (no implementada ni aprobada en todos sus detalles)
Django + PostgreSQL + Celery/Redis + Shopify Admin API. Mantener módulo proveedor aislado; posible app honeys_integration. Integración nativa con Shopify Admin es un requerimiento histórico ambiguo: confirmar si UI embebida o Django Admin es suficiente. La pregunta original planteaba app dentro de plt_seo versus proyecto independiente; no consta respuesta definitiva en material disponible.
Módulos:
- Config: cuenta/token y URL desde secrets/env; habilitación por tienda, modo TEST.
- Feed: descarga, validación, staging, normalización, importación incremental; identidad proveedor+SKU, asociación con variante Shopify; conservar contenido editorial propio; no eliminar automáticamente por ausencia en feed.
- Pricing: costo proveedor, moneda, MAP, reglas de margen y publicación; no sobrescribir sin validación. MAP no es costo.
- Inventory: stock por SKU y ubicación; un escritor por ubicación; inicialmente proveedor puede mantener sincronización nativa; stock pre-order por API.
- Shipping estimator: servicio separado, tarifas estimadas y reglas de embalaje.
- Orders: webhook Shopify validado, validar dirección/stock, agrupar líneas repetidas, referencia única persistente, enviar XML, registrar código y conciliar antes de reintentar POST ambiguo.
- Tracking: consultar estado, guardar transportista/servicio/tracking/freightcost; actualizar fulfillment Shopify cuando proceda, sin duplicar notificaciones.
- Monitoring: estado de jobs, errores, discrepancias, alertas; logs sin tokens ni PII.
Flujo: Feed → staging → catálogo Shopify; stock/precios → variantes; pedido Shopify → validación → estimador → aprobación/reglas → pedido proveedor → polling → fulfillment y conciliación.
Modelo sugerido: SupplierConfig, SupplierProduct, Offer/InventorySnapshot, ImportRun, ShippingEstimate, SupplierOrder, SupplierOrderLine, TrackingEvent. No es esquema final.

## Estimación de envío — investigación pendiente
No hay endpoint de cotización previa en documentos suministrados. RTSHOP selecciona tarifa económica pero no devuelve una estimación previa documentada.
Datos requeridos: almacén origen (ZIP), destino ZIP/país, peso y dimensiones reales de empaque, cantidades, reglas de combinación/cajas, unidades, divisor dimensional según transportista, servicios disponibles, recargos, tarifas negociadas del proveedor, dropship/handling y restricciones.
Fuentes candidatas, sin validar: datos del feed, información solicitada a Honey's Place, APIs de tarifas de UPS/FedEx/USPS o agregador, histórico freightcost.
Calcular peso facturable según servicio (máximo de peso real y dimensional cuando aplique), costo base + recargos + handling; calibrar estimados contra freightcost real. No asumir que tarifas públicas igualan las del proveedor. Separar USD/CAD, margen y reglas de checkout. Ante falta de datos, bloquear automatización o revisión manual, no prometer un importe exacto.

## Implementación y pruebas propuestas
- Fase 0: confirmar cuenta, feed real y esquema, mercados, modelo de credenciales y transporte.
- Fase 1: cliente XML seguro, fixtures mock, pruebas unitarias, feed staging e importación dry-run.
- Fase 2: precios/inventario, evitar doble escritor, reconciliación Shopify.
- Fase 3: estimador de transporte y validación previa.
- Fase 4: pedidos TEST, tracking, fulfillment, reintentos y duplicados.
- Fase 5: piloto controlado USA, observabilidad y operación.
SQLite puede servir para pruebas aisladas si se aprueba; validación final PostgreSQL. Mocks de Honey's y Shopify son propuesta histórica ante ausencia de credenciales; no sustituyen integración real. Probar 100/999/700/500/501/400/300 y demás errores, XML inválido, encoding, timeout, respuestas parciales, límite SKU, referencias TEST, token inválido y concurrencia. Desactivar DTD/entidades externas, verificar TLS, configurar timeout y backoff; no reenviar pedido ante timeout sin conciliación.
Criterios: importación idempotente, precios/MAP correctos, stock coherente, cotización identificada como estimación, una orden proveedor por referencia, tracking propagado, secretos fuera de Git.

## Preguntas históricas sin resolución comprobada
- App dentro de plt_seo o proyecto independiente.
- Diseño detallado original: obligatorio o guía.
- UI React/Liquid/templates embebida en Shopify Admin o Django Admin + env.
- SQLite aceptable en sandbox.
- Mocks y XML de ejemplo como estrategia de pruebas.
- Contrato real de feed, unidades, tarifas, permisos, rate limits, estados, cancelación y reembolsos.
No hay evidencia suficiente para afirmar que se haya implementado esta integración o que Honey's Place sea actualmente proveedor activo. No confundir con Nalpac o Sexy Living.

## Nota de preservación
Este Markdown consolida el contenido textual técnico y las decisiones recuperables, no reproduce capturas de pantalla del PDF ni adjunta los originales binarios. Las diferencias entre PDF y extracción histórica quedan señaladas; deben contrastarse con el proveedor antes de producción.
