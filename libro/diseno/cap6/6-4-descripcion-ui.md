# 6.4 Descripción de la interfaz de usuario

| Elemento | Dónde | Regla |
|---|---|---|
| Formulario de registro | Registro | correo válido y no usado; clave de 10 o más caracteres con letras y números; la primera cuenta es administradora y activa, las demás desarrolladoras pendientes de aprobación (RN-S01) |
| Formulario de ingreso | Ingreso | un solo mensaje para correo o clave incorrectos; tras 10 fallos, espera de 15 minutos (RNF-S01); una cuenta pendiente lee «Tu cuenta espera la aprobación de un administrador» y una desactivada, «Tu cuenta está desactivada: pide a un administrador que la reactive» |
| Menú lateral | todas las pantallas del panel | muestra las opciones del rol; el contador de *Usuarios* son los registros pendientes |
| Tabla de revisiones | Revisiones | más recientes primero; filtros por repositorio y estado; se refresca mientras hay revisiones pendientes o en análisis |
| Insignia de estado | Revisiones, Detalle | texto + icono + color para Pendiente, En análisis, Publicada · Aprobada, Publicada · Con problemas y Fallida |
| Resumen | Revisiones, Detalle | confirmados, posibles y descartados; no se muestra si la revisión no terminó; los archivos que no compilaron se avisan aparte (RN-S05) |
| Hallazgo | Detalle | archivo, línea:columna, clase, mensaje y ruta; enlace al archivo en el PR |
| Clasificación | Detalle | Sin revisar, Confirmado o Falso positivo; queda registrado quién la hizo y cuándo; un falso positivo deja de reportarse en las siguientes revisiones del repositorio (RN-S03) |
| Reintentar | Detalle | disponible en revisiones publicadas o fallidas; nunca en una en curso |
| Revisar un PR ahora | Revisiones | solo repositorios activos; si el commit ya se revisó, enlaza a esa revisión (RN-S02) |
| Conectar repositorio | Repositorios | nombre `propietario/nombre` único; política `Silent` o `Possibly`; bloqueo del merge |
| URL y secreto del *webhook* | modal tras conectar | solo los ve el administrador; botones para copiarlos |
| Acciones sobre usuarios | Usuarios | aprobar con rol (Pendiente → Activo), rechazar (Pendiente → Desactivado), desactivar y reactivar, cambiar rol; nadie vuelve a Pendiente; nunca sobre la propia cuenta |
| Confirmaciones | desactivar usuario, desconectar repositorio | dicen la consecuencia antes de hacerla |
| Errores | en el campo o en un aviso | el texto es el `mensaje` del error de la API, sin códigos técnicos |

Accesibilidad: cada campo tiene su etiqueta, los avisos usan `role="alert"`
o `role="status"`, los botones de solo icono tienen `aria-label` y el
contraste del texto es de al menos 4.5:1 en los dos temas.
