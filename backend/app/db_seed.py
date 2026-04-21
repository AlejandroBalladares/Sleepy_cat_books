from datetime import datetime, timedelta, timezone
from app.models.users import Rol, UsuarioRegistrar
import os

from app.models.books import LibroCrear, Reseña
from app.models.comunidad import ComunidadCrear, ImagenPublicacion, Publicacion, PublicacionCrear

seed_usuarios = []
seed_libros = []
seed_reseñas = []
seed_comunidades = []
seed_posts = []

# Some data can be used in testing and production
seed_generos = ["fantasia", "ciencia ficción", "romance", "policial", "aventura", "biografía", "misterio", "ficción"]

# Add data for 'test' only
if os.getenv("AUTOMATED_TESTS", None):
    from faker import Faker

    fake = Faker()

    seed_usuarios = [
        UsuarioRegistrar( # ID 1
            nombre="Bob",
            apellido="Robinson",
            email="bob@company.com",
            contraseña="valid-passw0rd",
            fecha_nacimiento=fake.date_of_birth(minimum_age=20),
            nombre_de_usuario=fake.user_name(),
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 2
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            email="alice@company.com",
            contraseña="valid-passw0rd",
            fecha_nacimiento=fake.date_of_birth(minimum_age=20),
            nombre_de_usuario=fake.user_name(),
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 3
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            email=fake.email(),
            contraseña=fake.password(length=10),
            fecha_nacimiento=fake.date_of_birth(minimum_age=30),
            nombre_de_usuario=fake.user_name(),
            rol=Rol.AUTOR
        )
    ]

    seed_libros = [
        LibroCrear(
            nombre="Harry Potter",
            descripcion=fake.text(max_nb_chars=20),
            fecha_publicacion=fake.date(),
            generos=["fantasia"],
            id_autor=1,
            isbn=fake.isbn10(),
            portada="http://portada.com"
        ),
        LibroCrear(
            nombre="El Principito",
            descripcion=fake.text(max_nb_chars=20),
            fecha_publicacion=fake.date(),
            generos=["fantasia"],
            id_autor=3,
            isbn=fake.isbn10(),
            portada="http://portada.com"
        ),
        LibroCrear(
            nombre="Memoirs of a Geisha",
            descripcion=fake.text(max_nb_chars=20),
            fecha_publicacion=fake.date(),
            generos=["romance"],
            id_autor=1,
            isbn=fake.isbn10(),
            portada="http://portada.com"
        ),
        LibroCrear(
            nombre="The Adventures of Sherlock Holmes",
            descripcion=fake.text(max_nb_chars=20),
            fecha_publicacion=fake.date(),
            generos=["misterio"],
            id_autor=3,
            isbn=fake.isbn10(),
            portada="http://portada.com"
        )
    ]

    seed_reseñas = [
        Reseña(id_usuario=1, id_libro=1, contenido="Very good book"),
        Reseña(id_usuario=3, id_libro=1, contenido="Cool book"),
        Reseña(id_usuario=1, id_libro=2, contenido="Very good book"),
    ]

    seed_comunidades = [
        ComunidadCrear(
            nombre="Lectores de Ciencia Ficción",
            descripcion="Comunidad para los amantes de la ciencia ficción",
            id_creador=1
        ),
        ComunidadCrear(
            nombre="Lectores de Romance",
            descripcion="Comunidad para los amantes de las historias de amor",
            id_creador=2
        ),
        ComunidadCrear(
            nombre="Lectores de Aventura",
            descripcion="Comunidad para los amantes de las historias de aventura",
            id_creador=1
        )
    ] 
elif os.getenv("TESTING"):
    from faker import Faker
    from app.testing.books import create_book
    from app.testing.reviews import create_review
    from app.testing.communities import create_community
    from app.testing.users import create_user

    fake = Faker()

    # add 10 random users
    for _ in range(10):
        seed_usuarios.append(create_user(fake))
    
    # add 10 random communities
    for _ in range(10):
        seed_comunidades.append(create_community(fake, len(seed_usuarios)))

    # add 21 random books
    for _ in range(21):
        seed_libros.append(create_book(fake, len(seed_usuarios), seed_generos))

    # add 100 random reviews
    for _ in range(100):
        seed_reseñas.append(create_review(fake, len(seed_usuarios), len(seed_libros)))

else: # This data is for 'prod'
    seed_usuarios = [
        UsuarioRegistrar( # ID 1
            nombre="Joanne",
            apellido="Rowling",
            contraseña="itsmagic",
            email="jkrowling@magician.com",
            fecha_nacimiento=datetime(1965, 7, 31),
            nombre_de_usuario="jkrowling",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 2
            nombre="Alice",
            apellido="Kingston",
            contraseña="super-password",
            email="alice_kingston_90@company.com",
            fecha_nacimiento=datetime(1990, 5, 4),
            nombre_de_usuario="alice_k",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 3
            nombre="Bob",
            apellido="Robinson",
            contraseña="best_p4ss",
            email="bob_rob@university.com",
            fecha_nacimiento=datetime(1994, 7, 20),
            nombre_de_usuario="bobby94",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 4
            nombre="George",
            apellido="Martin",
            contraseña="winteriscoming",
            email="grrm@dragon.com",
            fecha_nacimiento=datetime(1948, 9, 20),
            nombre_de_usuario="grrmartin",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 5
            nombre="Arthur Conan",
            apellido="Doyle",
            contraseña="elemental",
            email="acdoyle@detective.com",
            fecha_nacimiento=datetime(1859, 5, 22),
            nombre_de_usuario="acdoyle",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 6
            nombre="Juana",
            apellido="D'Arc",
            contraseña="betterthananyone",
            email="juanadarc@googlemail.com",
            fecha_nacimiento=datetime(2001, 7, 12),
            nombre_de_usuario="DarkJ",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 7
            nombre="Sofía",
            apellido="Martínez",
            contraseña="cofferainbook",
            email="sofimarti95@mail.com",
            fecha_nacimiento=datetime(1995, 2, 4),
            nombre_de_usuario="romanticlover",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 8
            nombre="Matías",
            apellido="Gallardo",
            contraseña="loveandpeace",
            email="matiasg@googlemail.com",
            fecha_nacimiento=datetime(2004, 9, 20),
            nombre_de_usuario="occasional.reader",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 9
            nombre="Facundo",
            apellido="Asimov",
            contraseña="bladerunner",
            email="fasimov@writer.com",
            fecha_nacimiento=datetime(1995, 12, 1),
            nombre_de_usuario="Asimov",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 10
            nombre="Roberto A.",
            apellido="Nonimo",
            contraseña="dogsandbike",
            email="ranonimo@nobody.com",
            fecha_nacimiento=datetime(1998, 8, 13),
            nombre_de_usuario="NotAn0n",
            rol=Rol.AUTOR
        ),
        UsuarioRegistrar( # ID 11
            nombre="Jazmín",
            apellido="Blanca",
            contraseña="jazminblanca",
            email="jblanca@email.com",
            fecha_nacimiento=datetime(1965, 5, 25),
            nombre_de_usuario="historyteacher",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 12
            nombre="Mr.",
            apellido="Magoo",
            contraseña="novenove",
            email="mrmagoo@ofice.com",
            fecha_nacimiento=datetime(1985, 3, 30),
            nombre_de_usuario="Mr_Magoo",
            rol=Rol.LECTOR
        ),
        UsuarioRegistrar( # ID 13
            nombre="One",
            apellido="Only",
            contraseña="mybiography",
            email="onlyone@onlyone.com",
            fecha_nacimiento=datetime(1987, 5, 2),
            nombre_de_usuario="onlyone",
            rol=Rol.AUTOR
        )
    ]

    seed_libros = [
        LibroCrear( # ID 1
            nombre="Harry Potter and the Philosopher's Stone",
            descripcion="""Harry Potter thinks he is an ordinary boy - until he is rescued by an owl, taken to Hogwarts School of Witchcraft and Wizardry, learns to play Quidditch and does battle in a deadly duel. The Reason ... HARRY POTTER IS A WIZARD!
""",
            fecha_publicacion=datetime(1997, 6, 26),
            generos=["fantasia"],
            id_autor=1,
            isbn="9780747532699",
            portada="https://upload.wikimedia.org/wikipedia/en/6/6b/Harry_Potter_and_the_Philosopher%27s_Stone_Book_Cover.jpg"
        ),
        LibroCrear( # ID 2
            nombre="A Game of Thrones (A Song of Ice and Fire, #1)",
            descripcion="""Long ago, in a time forgotten, a preternatural event threw the seasons out of balance. In a land where summers can last decades and winters a lifetime, trouble is brewing. The cold is returning, and in the frozen wastes to the north of Winterfell, sinister forces are massing beyond the kingdom's protective Wall. To the south, the king's powers are failing—his most trusted adviser dead under mysterious circumstances and his enemies emerging from the shadows of the throne. At the center of the conflict lie the Starks of Winterfell, a family as harsh and unyielding as the frozen land they were born to. Now Lord Eddard Stark is reluctantly summoned to serve as the king's new Hand, an appointment that threatens to sunder not only his family but the kingdom itself.

Sweeping from a harsh land of cold to a summertime kingdom of epicurean plenty, A Game of Thrones tells a tale of lords and ladies, soldiers and sorcerers, assassins and bastards, who come together in a time of grim omens. Here an enigmatic band of warriors bear swords of no human metal; a tribe of fierce wildlings carry men off into madness; a cruel young dragon prince barters his sister to win back his throne; a child is lost in the twilight between life and death; and a determined woman undertakes a treacherous journey to protect all she holds dear. Amid plots and counter-plots, tragedy and betrayal, victory and terror, allies and enemies, the fate of the Starks hangs perilously in the balance, as each side endeavors to win that deadliest of conflicts: the game of thrones.
            """,
            fecha_publicacion=datetime(1996, 8, 6),
            generos=["fantasia", "aventura", "ficción"],
            id_autor=4,
            isbn="0553588486",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1562726234i/13496.jpg"
        ),
        LibroCrear( # ID 3
            nombre="A Study in Scarlet",
            descripcion="""Our first meeting with Sherlock Holmes. And John Watson's too! The young doctor is astonished by Holmes' many idiosyncrasies, including his talents on the violin.

But it's not long before Sherlock Holmes, with Watson in tow, is working with Scotland Yard investigating the murder of two Americans whose deaths have some mysterious connection to sinister groups gathering power in both Britain and America.

Here's where it all began, 'A Study in Scarlet.' Meet Sherlock Holmes, one of the world's leading consulting detectives - fictional of course!
""",
            fecha_publicacion=datetime(1887, 1, 1),
            generos=["misterio", "ficción"],
            id_autor=5,
            isbn="1420925539",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1519031842i/102868.jpg"
        ),
        LibroCrear( # ID 4
            nombre="The Eclipse",
            descripcion="""Prepare yourself for a journey of love, duty, and destiny as Alina steps into her role, poised on the brink of war. The adventure continues, with the stakes higher than ever, as we encounter new friends and formidable foes.
""",
            fecha_publicacion=datetime(2024, 9, 14),
            generos=["romance"],
            id_autor=10,
            isbn="0061730866",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1726374839i/219191097.jpg"
        ),
        LibroCrear( # ID 5
            nombre="Lost and Lassoed",
            descripcion="""Teddy Andersen doesn't have a plan. She's never needed one before. She's always been more of a go with the flow type of girl, but for some reason, the flow doesn't seem to be going her way this time.

Her favorite vintage suede jacket has a hole in it, her sewing machine is broken, and her best friend just got engaged. Suddenly, everything feels like it's starting to change. Teddy's used to being a leader, but now she feels like she's getting left behind, wondering if life in the small town she loves is enough for her anymore.

Gus Ryder has a lot on his plate. He doesn't know what's taking care of his family's 8,000 acre ranch, or parenting his spunky six-year-old daughter, who is staying with him for the summer. Gus has always been the dependable one, but when his workload starts to overwhelm him, he has to admit that he can't manage everything on his own. He needs help.

His little sister's best friend, the woman he can't stand, is not who he had in mind. But when no one else can step in, Teddy's the only option he's got. Teddy decides to use the summer to try and figure out what she wants out of life. Gus, on the other hand, starts to worry that he'll never find what he needs.

Tempers flare, tension builds, and for the first time ever, Gus and Teddy start to see each other in a different light. As new feelings start to simmer below the surface, they must decide whether or not to act on them. Can they keep things cool? Or will both of them get burned?
""",
            fecha_publicacion=datetime(2024, 11, 5),
            generos=["romance", "ficción"],
            id_autor=10,
            isbn="0593732456",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1709824283i/207611511.jpg"
        ),
        LibroCrear( # ID 6
            nombre="Make the Season Bright",
            descripcion="""Two exes find themselves stuck at the same house for Christmas in this holiday romance by Ashley Herring Blake, USA Today bestselling author of Iris Kelly Doesn't Date.

It's been five years since Charlotte Donovan was ditched at the altar by her ex-fiancée, and she's doing more than okay. Sure, her single mother never checks in, but she has her strings ensemble, the Rosalind Quartet, and her life in New York is a dream come true. As the holidays draw near, her ensemble mate Sloane persuades Charlotte and the rest of the quartet to spend Christmas with her family in Colorado—it is much cozier and quieter than Manhattan, and it would guarantee more practice time for the quartet's upcoming tour. But when Charlotte arrives, she discovers that Sloane's sister Adele also brought a friend home—and that friend is none other than her ex, Brighton. All Brighton Fairbrook wanted was to have the holliest, jolliest Christmas—and try to forget that her band kicked her out. But instead, she's stuck pretending like she and her ex are strangers—which proves to be difficult when Sloane and Adele's mom signs them all up for a series of Christmas dating events. Charlotte and Brighton are soon entrenched in horseback riding and cookie decorating, but Charlotte still won't talk to her. Brighton can hardly blame her after what she did. After a few days, however, things start to slip through. Memories. Music. The way they used to play together—Brighton on guitar, Charlotte on her violin—and it all feels painfully familiar. But it's all in the past and nothing can melt the ice in their hearts...right?
""",
            fecha_publicacion=datetime(2024, 10, 1),
            generos=["romance", "ficción"],
            id_autor=10,
            isbn="0593550595",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1706587212i/206180603.jpg"
        ),
        LibroCrear( # ID 7
            nombre="Dune",
            descripcion="""Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only thing of value is the “spice” melange, a drug capable of extending life and enhancing consciousness. Coveted across the known universe, melange is a prize worth killing for...
""",
            fecha_publicacion=datetime(2019, 10, 1),
            generos=["ciencia ficción", "fantasia", "aventura"],
            id_autor=9,
            isbn="0074748335380",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1555447414i/44767458.jpg"
        ),
        LibroCrear( # ID 8
            nombre="Fahrenheit 451",
            descripcion="""Guy Montag is a fireman. His job is to destroy the most illegal of commodities, the printed book, along with the houses in which they are hidden. Montag never questions the destruction and ruin his actions produce, returning each day to his bland life and wife, Mildred, who spends all day with her television “family.” But when he meets an eccentric young neighbor, Clarisse, who introduces him to a past where people didn’t live in fear and to a present where one sees the world through the ideas in books instead of the mindless chatter of television, Montag begins to question everything he has ever known.
""",
            fecha_publicacion=datetime(2010, 10, 19),
            generos=["ciencia ficción", "fantasia", "ficción"],
            id_autor=9,
            isbn="9780743247221",
            portada="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1351643740i/4381.jpg"
        ),
        LibroCrear( # ID 9
            nombre="My biography",
            descripcion="La historia de mi vida...",
            fecha_publicacion=datetime(2023, 9, 21),
            generos=["biografía"],
            id_autor=13,
            isbn="4321167890234",
            portada="https://imgs.search.brave.com/w-5fiKvhZYLady5MZPIO5xvxoBl8Otqb3Fo6tZXc59M/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vYmxhZGVu/b25saW5lLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAyMS8w/My9CaW9ncmFwaHkt/MS5wbmc_Zml0PTEw/ODAsMTA4MCZzc2w9/MQ"
        )
    ]

    seed_reseñas = [
        Reseña(id_usuario=1, id_libro=1, contenido="El mejor libro que leí en mi vida, super recomendado. Es tan bueno que hasta pareciera que lo escribí yo. :)"),
        Reseña(id_usuario=3, id_libro=1, contenido="Buen libro, me gustó la parte de la magia."),
        Reseña(id_usuario=3, id_libro=2, contenido="Pudo haber sido mejor, veremos si la segunda parte mejora..."),
        Reseña(id_usuario=7, id_libro=6, contenido="Ameeee, excelente libro, lo super recomiendo <3"),
        Reseña(id_usuario=7, id_libro=5, contenido="Ayy el final fue muy lindo, lloré por una semana, me encantó :')"),
        Reseña(id_usuario=6, id_libro=1, contenido="Aburrido, encima la autora se auto califica como que fue un buen libro, no lo recomiendo")
    ]

    seed_comunidades = [
        ComunidadCrear( # ID 1
            nombre="Lectores de Ciencia Ficción",
            descripcion="Comunidad para los amantes de la ciencia ficción",
            id_creador=9,
            imagen="https://i.blogs.es/fa5919/a909c82c94b8330ece6768267f93c6cd/1366_2000.jpg"
        ),
        ComunidadCrear( # ID 2
            nombre="Lectores de Romance",
            descripcion="Comunidad para los amantes de las historias de amor",
            id_creador=7
        ),
        ComunidadCrear( # ID 3
            nombre="Lectores de Misterio",
            descripcion="Comunidad para los amantes de las historias de misterio",
            id_creador=5
        )
    ]

    seed_posts = [
        Publicacion(id_usuario=9, id_comunidad=1, fecha=datetime.now(timezone.utc) - timedelta(hours=5),
            contenido="Bienvenid@s amantes de la ciencia ficción a esta fabulosa comunidad :)", imagenes=[
            ImagenPublicacion(url="https://i.blogs.es/6572fc/81opykuzkjl/1366_2000.jpeg"),
            ImagenPublicacion(url="https://i.blogs.es/e05471/71ub2nwhejl/1366_2000.jpg"),
            ImagenPublicacion(url="https://i.blogs.es/016242/dune/1366_2000.jpg")
        ]),
        Publicacion(id_usuario=7, id_comunidad=2, fecha=datetime.now(timezone.utc) - timedelta(hours=1),
            contenido="¡¡¡Holaaa a todos los amantes de romance!!! Sean bienvenidos a esta increíble comunidad. Los invito a presentarse y compartir sus libros favoritos. :D",
        ),
    ]
