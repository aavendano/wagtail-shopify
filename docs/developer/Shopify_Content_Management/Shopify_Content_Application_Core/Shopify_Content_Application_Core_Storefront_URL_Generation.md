# Generación de URL de Escaparate de Shopify

Este módulo, `Shopify_Content_Application_Core_Storefront_URL_Generation`, es fundamental para la construcción y gestión de rutas URL canónicas para las páginas de contenido de Wagtail dentro de la aplicación de Shopify. Facilita la generación consistente de URL para varios tipos de contenido, asegurando que el contenido sea accesible a través de rutas de escaparate de Shopify bien definidas, incluyendo variantes específicas de localización.

## Propósito y Funcionalidad Principal

El módulo se centra en proporcionar un conjunto de funciones y una clase de datos para:
1.  Generar rutas de URL relativas al escaparate para diferentes tipos de contenido (productos, colecciones, blogs, artículos, términos de glosario, páginas de ubicación y páginas de inicio).
2.  Manejar los prefijos de localización (Mercados de Shopify) para las URL, permitiendo rutas específicas de idioma/región.
3.  Normalizar y recopilar diferentes variantes de ruta para fines de indexación.

### Componentes Clave

#### `PathVariant`
Este es un dataclass que encapsula una variante de ruta de escaparate.

```python
@dataclass(frozen=True)
class PathVariant:
    normalized_path: str
    locale_prefix: str
    is_canonical: bool
```

*   `normalized_path`: La ruta del escaparate normalizada (sin prefijo de localización).
*   `locale_prefix`: El prefijo de localización (por ejemplo, 'es-us') si aplica, de lo contrario una cadena vacía.
*   `is_canonical`: Un booleano que indica si esta variante es la ruta canónica principal.

#### Funciones de Generación de Rutas

El módulo proporciona funciones específicas para generar rutas para cada tipo de contenido:

*   `product_path(handle: str) -> str`: Genera una ruta para un producto.
*   `collection_path(handle: str) -> str`: Genera una ruta para una colección.
*   `blog_path(handle: str) -> str`: Genera una ruta para un blog.
*   `article_path(blog_handle: str, article_handle: str) -> str`: Genera una ruta para un artículo dentro de un blog.
*   `glossary_term_path(handle: str) -> str`: Genera una ruta para un término de glosario.
*   `location_page_path(handle: str) -> str`: Genera una ruta para una página de ubicación.
*   `home_page_path(handle: str) -> str`: Genera una ruta para una página de inicio.
*   `metaobject_page_path(url_handle: str, handle: str) -> str`: Genera una ruta para una página de metaobjeto genérica.
*   `root_index_path(slug: str) -> str | None`: Devuelve la ruta de índice para un slug raíz conocido.
*   `related_link_path(link: dict[str, Any]) -> str`: Construye una URL relativa al escaparate a partir de un diccionario de enlace relacionado serializado.

#### Funciones Auxiliares y Lógica Central

*   `_page_handle(page) -> str`: Extrae el 'handle' o slug de una página.
*   `page_content_type_key(page) -> str | None`: Determina una clave de tipo de contenido estable para una página de Wagtail, mapeando los modelos de página a claves de cadena (e.g., 'product', 'article'). Para más detalles sobre los modelos de página, consulte [Modelos de Página de Contenido](../Content_Page_Models.md).
*   `_article_blog_handle(page) -> str`: Obtiene el 'handle' del blog padre para una `ArticlePage`.
*   `_location_handle(page) -> str`: Obtiene el 'handle' de la ubicación para una `LocationPage`.
*   `_home_handle(page) -> str`: Obtiene el 'handle' de la página de inicio para una `HomePage`.
*   `storefront_path_for_page(page) -> str | None`: La función central que devuelve la ruta canónica relativa al escaparate para cualquier página de Wagtail dada, utilizando las funciones de generación de rutas específicas y los modelos de página para determinar el tipo de contenido.
*   `locale_prefix_for_page(page) -> str`: Recupera el prefijo de URL de los Mercados de Shopify para la localización de la página, si está disponible.
*   `page_index_metadata(page) -> tuple[str, str, str]`: Devuelve una tupla que contiene el tipo de contenido, el 'handle' y el 'blog_handle' (para artículos) para su uso en la indexación de URL.
*   `path_variants_for_index(page) -> list[PathVariant]`: Genera una lista de objetos `PathVariant` para una página, incluyendo la ruta canónica y cualquier variante con prefijo de localización.
*   `all_paths_for_page(page) -> list[str]`: Devuelve una lista de todas las rutas de escaparate relativas completas para una página, incluyendo las rutas canónicas y con prefijo de localización.

## Arquitectura y Relaciones de Componentes

El módulo `shopify_content/storefront_urls.py` actúa como un orquestador para la generación de URL, dependiendo en gran medida de los modelos de página de Wagtail definidos en el módulo [Modelos de Página de Contenido](../Content_Page_Models.md) para determinar el tipo de contenido y extraer los datos relevantes (`handle`, `slug`, `locale`).

```mermaid
graph TD
    A[shopify_content/storefront_urls.py] --> B(Objeto de Página Wagtail)
    B -- Determina Tipo y Extrae Datos --> C[Funciones de Generación de Rutas]
    C --> D(storefront_path_for_page)
    D --> E(PathVariant)
    D --> F(locale_prefix_for_page)
    F --> E
    E --> G(path_variants_for_index)
    G --> H(all_paths_for_page)

    subgraph Modelos de Contenido Wagtail
        B -- Utiliza --> I[Modelos de Página (ej. ArticlePage, HomePage)]
    end

    style A fill:#ace,stroke:#333,stroke-width:2px
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:2px
    style D fill:#fff,stroke:#333,stroke-width:2px
    style E fill:#ccf,stroke:#333,stroke-width:2px
    style F fill:#afa,stroke:#333,stroke-width:2px
    style G fill:#fff,stroke:#333,stroke-width:2px
    style H fill:#fff,stroke:#333,stroke-width:2px
    style I fill:#eee,stroke:#333,stroke-width:2px
```


    linkStyle 173 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 174 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 175 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 176 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 177 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 178 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 179 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 180 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 181 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 182 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 183 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 184 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 185 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 186 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 187 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 188 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 189 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 190 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 191 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 192 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 193 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 194 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 195 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 196 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 197 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 198 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 199 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 200 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 201 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 202 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 203 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 204 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 205 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 206 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 207 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 208 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 209 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 210 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 211 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 212 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 213 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 214 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 215 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 216 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 217 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 218 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 219 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 220 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 221 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 222 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 223 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 224 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 225 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 226 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 227 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 228 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 229 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 230 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 231 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 232 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 233 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 234 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 235 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 236 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 237 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 238 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 239 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 240 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 241 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 242 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 243 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 244 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 245 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 246 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 247 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 248 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 249 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 250 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 251 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 252 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 253 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 254 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 255 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 256 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 257 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 258 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 259 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 260 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 261 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 262 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 263 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 264 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 265 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 266 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 267 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 268 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 269 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 270 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 271 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 272 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 273 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 274 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 275 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 276 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 277 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 278 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 279 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 280 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 281 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 282 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 283 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 284 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 285 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 286 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 287 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 288 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 289 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 290 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 291 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 292 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 293 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 294 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 295 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 296 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 297 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 298 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 299 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 300 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 301 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 302 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 303 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 304 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 305 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 306 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 307 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 308 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 309 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 310 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 311 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 312 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 313 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 314 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 315 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 316 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 317 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 318 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 319 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 320 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 321 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 322 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 323 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 324 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 325 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 326 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 327 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 328 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 329 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 330 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 331 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 332 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 333 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 334 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 335 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 336 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 337 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 338 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 339 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 340 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 341 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 342 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 343 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 344 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 345 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 346 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 347 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 348 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 349 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 350 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 351 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 352 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 353 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 354 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 355 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 356 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 357 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 358 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 359 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 360 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 361 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 362 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 363 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 364 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 365 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 366 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 367 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 368 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 369 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 370 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 371 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 372 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 373 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 374 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 375 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 376 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 377 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 378 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 379 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 380 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 381 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 382 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 383 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 384 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 385 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 386 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 387 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 388 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 389 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 390 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 391 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 392 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 393 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 394 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 395 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 396 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 397 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 398 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 399 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 400 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 401 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 402 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 403 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 404 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 405 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 406 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 407 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 408 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 409 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 410 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 411 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 412 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 413 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 414 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 415 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 416 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 417 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 418 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 419 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 420 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 421 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 422 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 423 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 424 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 425 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 426 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 427 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 428 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 429 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 430 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 431 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 432 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 433 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 434 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 435 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 436 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 437 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 438 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 439 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 440 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 441 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 442 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 443 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 444 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 445 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 446 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 447 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 448 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 449 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 450 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 451 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 452 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 453 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 454 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 455 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 456 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 457 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 458 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 459 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 460 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 461 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 462 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 463 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 464 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 465 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 466 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 467 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 468 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 469 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 470 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 471 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 472 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 473 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 474 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 475 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 476 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 477 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 478 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 479 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 480 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 481 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 482 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 483 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 484 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 485 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 486 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 487 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 488 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 489 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 490 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 491 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 492 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 493 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 494 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 495 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 496 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 497 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 498 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 499 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 500 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 501 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 502 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 503 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 504 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 505 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 506 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 507 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 508 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 509 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 510 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 511 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 512 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 513 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 514 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 515 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 516 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 517 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 518 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 519 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 520 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 521 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 522 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 523 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 524 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 525 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 526 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 527 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 528 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 529 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 530 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 531 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 532 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 533 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 534 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 535 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 536 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 537 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 538 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 539 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 540 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 541 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 542 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 543 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 544 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 545 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 546 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 547 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 548 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 549 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 550 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 551 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 552 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 553 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 554 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 555 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 556 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 557 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 558 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 559 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 560 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 561 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 562 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 563 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 564 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 565 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 566 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 567 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 568 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 569 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 570 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 571 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 572 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 573 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 574 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 575 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 576 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 577 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 578 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 579 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 580 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 581 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 582 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 583 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 584 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 585 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 586 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 587 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 588 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 589 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 590 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 591 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 592 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 593 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 594 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 595 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 596 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 597 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 598 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 599 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 600 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 601 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 602 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 603 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 604 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 605 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 606 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 607 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 608 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 609 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 610 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 611 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 612 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 613 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 614 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 615 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 616 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 617 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 618 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 619 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 620 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 621 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 622 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 623 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 624 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 625 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 626 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 627 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 628 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 629 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 630 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 631 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 632 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 633 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 634 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 635 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 636 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 637 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 638 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 639 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 640 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 641 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 642 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 643 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 644 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 645 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 646 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 647 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 648 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 649 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 650 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 651 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 652 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 653 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 654 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 655 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 656 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 657 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 658 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 659 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 660 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 661 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 662 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 663 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 664 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 665 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 666 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 667 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 668 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 669 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 670 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 671 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 672 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 673 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 674 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 675 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 676 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 677 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 678 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 679 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 680 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 681 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 682 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 683 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 684 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 685 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 686 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 687 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 688 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 689 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 690 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 691 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 692 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 693 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 694 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 695 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 696 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 697 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 698 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 699 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 700 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 701 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 702 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 703 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 704 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 705 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 706 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 707 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 708 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 709 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 710 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 711 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 712 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 713 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 714 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 715 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 716 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 717 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 718 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 719 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 720 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 721 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 722 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 723 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 724 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 725 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 726 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 727 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 728 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 729 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 730 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 731 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 732 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 733 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 734 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 735 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 736 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 737 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 738 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 739 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 740 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 741 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 742 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 743 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 744 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 745 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 746 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 747 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 748 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 749 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 750 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 751 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 752 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 753 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 754 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 755 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 756 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 757 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 758 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 759 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 760 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 761 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 762 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 763 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 764 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 765 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 766 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 767 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 768 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 769 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 770 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 771 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 772 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 773 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 774 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 775 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 776 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 777 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 778 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 779 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 780 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 781 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 782 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 783 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 784 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 785 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 786 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 787 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 788 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 789 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 790 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 791 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 792 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 793 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 794 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 795 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 796 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 797 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 798 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 799 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 800 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 801 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 802 stroke:#666,stroke-width:1px,fill:none;
    linkStyle 83 stroke:#666,stroke-width:1px,fill:none;
