![Pokedéx](static/pokemon2.webp)

# 📘 Pokédex Interactiva

Una aplicación web interactiva que permite explorar Pokémon mediante una galería visual obtenida desde la API oficial de PokéAPI. Los usuarios pueden buscar, filtrar y guardar sus Pokémon favoritos luego de registrarse.

## 🎮 Funcionalidades principales

- 🔍 **Búsqueda por nombre**: Ingresa el nombre de un Pokémon y encontralo al instante.
- 🔥💧🌿 **Filtrado por tipo**: Visualiza Pokémon de tipo fuego, agua o planta.
- ⭐ **Favoritos**: Si estás registrado y logueado, podés marcar tus Pokémon favoritos.
- 👤 **Registro e inicio de sesión**: Crea tu cuenta y accedé a funcionalidades extra.
- 🎨 **Interfaz temática**: Inspirada en el universo Pokémon para una experiencia inmersiva.

---

## 🚀 ¿Cómo acceder a la Pokédex localmente?

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/pokedex.git
   cd pokedex
   
2. Instala los paquetes necesarios:   
   pip install -r requirements.txt
   
3. Ejecuta el servidor de desarrollo:
   python manage.py runserver
   
5. Ingresa a http://localhost:3000 en tu navegador.

⚠️ ¿Qué hacer si la app se cierra por error?
Si intentas agregar el mismo Pokémon a favoritos más de una vez, puede que se cierre la app o se muestre un mensaje de error.
-Refresca la página (F5) y continuá navegando normalmente.

📁 Estructura principal del proyecto
├── app/
│   ├── templates/      # HTMLs de la app
│   ├── static/         # Archivos CSS, imágenes
│   ├── layers/
│   │   ├── services/   # Lógica de negocio
│   │   ├── persistence/
│   │   ├── transport/
│   └── views.py        # Vistas Django
├── manage.py
├── README.md
└── requirements.txt

👩‍💻 Autor:
Desarrollado por Kaira Abréu
Proyecto educativo para la Tecnicatura en Informática

🌟 ¡Gracias por visitar esta Pokedéx! 🌟



   
