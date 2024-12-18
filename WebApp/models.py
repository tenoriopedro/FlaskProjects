from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
import sqlite3
from pathlib import Path


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    return db.session.get(Users, int(user_id))

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self,first_name, last_name, username, password):

        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        # Verifica se a password do banco de dados é igual que o usuário digitou
        return check_password_hash(self.password, password)


class Reservations(db.Model):
    __bind_key__ = 'reservations'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    car_name = db.Column(db.String(100), nullable=False)
    pick_up_date = db.Column(db.String(80), nullable=False)
    drop_off_date = db.Column(db.String(80), nullable=False)
    days = db.Column(db.Integer, nullable=False)

    def __init__(self, username, client_name, car_name, pick_up_date, drop_off_date, days):

        self.username = username
        self.client_name = client_name
        self.car_name = car_name
        self.pick_up_date = pick_up_date
        self.drop_off_date = drop_off_date
        self.days = days


class PaymentData(db.Model):
    __bind_key__ = 'payment_data'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    card_holder = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.String(80), nullable=False)
    cvc = db.Column(db.Integer, nullable=False)

    def __init__(self, username, card_holder, email, card_number, expiration_date, cvc):

        self.username = username
        self.card_holder = card_holder
        self.email = email
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvc = cvc


# iniciando banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()



####  CRIAÇÃO DA BASE DE DADOS DOS VEICULOS ####

# Caminho raiz do projeto
ROOT_DIR = Path(__file__).parent

# Nome da base de dados
DB_NAME = 'vehicles.db'

# Caminho absoluto da base de dados
DB_FILE = ROOT_DIR / 'database' / DB_NAME

# nome tabelas
TABLE_CARS = 'cars'
TABLE_MOTORCYCLES = 'motorcycles'


# Conexão com a base de dados
connection = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = connection.cursor()

# Vão ser criadas duas tabelas('cars', 'motorcycles') dentro da base de dados 'vehicles'
# para uma melhor manipulação dos dados, pois carros e motos tem especificações diferentes

# Dados da tabela_carros 'cars'
cars_data = [

    # gold
    ['BMW X6', 5, 5, 'auto', 'suv', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://purepng.com/public/uploads/large/purepng.com-bmw-x6-blue-carcarbmwvehicletransport-9615246630450hbgr.png'],
    ['Mercedes GLE coupe', 5, 5, 'auto', 'suv', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://www.mercedes-benz.pt/content/dam/hq/passengercars/cars/gle/gle-coupe-c167-fl-pi/modeloverview/01-2023/images/mercedes-benz-gle-coupe-c167-modeloverview-696x392-01-2023.png'],
    ['Audi Q8', 5, 5, 'auto', 'suv', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://www.pngmart.com/files/22/Audi-Q8-PNG-Isolated-Image.png'],
    ['Jaguar I-Pace', 5, 5, 'auto', 'suv', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://ymimg1.b8cdn.com/resized/car_model/7913/pictures/7416563/mobile_listing_main_Jaguar_I-Pace_2019__1_.png'],
    ['Porsche Cayenee Coupe',5, 5, 'auto', 'suv', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://www.pngmart.com/files/22/Porsche-Cayenne-PNG-Clipart.png'],
    ['BWM i7', 5, 5, 'auto', 'sedan', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://prod.cosy.bmw.cloud/bmwweb/cosySec?COSY-EU-100-7331cqgv2Z7d%25i02uCaY3MuO2kOHUtWPfbYfQn8N10tLhu1XzWVo7puMLWFmdkAj5DOPitIqZ8XgY1nTNIowJ4HO3zkyXq%25sGM8snpq6v6ODubLz2aKqfkYvjmB2fJj5DOP5Eagd%25kcWExHWpbl8FO2k3Hy2o24tXATQBrXpFkahlZ24riIqM8scpF4HvmnU0KiIFJG7dUABHvIT91QsO2JGvloRqCgpT9GsLxSQUilo90yWdBbHsLoACeV%25hJ0yLOEjkpqTACygN6nmmlOECUkw5O7sgNEbn%257b10UkNh5ucSVAbnkq83aBzOh5nmPXRYagq857Mrv1RUmP81D5Pixb7MPVY8%25MWh1DMztPOpeqVYDafuiwjmztYRS3Qc67aftxdXZiw1RSfWQxy%25%25VxdSeZLjYuzWQdjcnmj3aeZQ6KjPpXRjcZwB81vrx6Kc%252PVQ4WsKokGpc1Q8CBsJdoSWZ35uMwCRL'],
    ['Audi e-Tron GT', 5, 5, 'auto', 'sedan', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://www.electrifying.com/files/NFeDtk7gtILNVgt4/AudietronGT.png'],
    ['Mercedes CLS', 5, 5, 'auto', 'sedan', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://www.mercedes-benz.pt/content/dam/hq/passengercars/cars/cls/cls-coupe-c257-fl-pi/modeloverview/11-2022/images/mercedes-benz-cls-c257-modeloverview-696x392-11-2022.png'],
    ['Jaguar F-Type', 2, 2, 'auto', 'sedan', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://freepngimg.com/thumb/jaguar/24597-2-jaguar-f-type.png'],
    ['Porsche Taycan', 5, 5, 'auto', 'sedan', 'gold', True, 100, '2024-01-01', '2024-02-01', 'https://file.kelleybluebookimages.com/kbb/base/evox/CP/15460/2024-Porsche-Taycan-front_15460_032_2400x1800_2Y.png'],

    # silver
    ['Nissan Qashqai', 5, 5, 'manual', 'suv', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.greenncap.com/wp-content/uploads/nissan-qashqai-2022-0109.png'],
    ['Peugeot 3008', 5, 5, 'manual', 'suv', 'silver', True, 60, '2024-01-01', '2024-02-01',  'https://i.pinimg.com/originals/da/90/f0/da90f0319bd65df5051158e1d4bab041.png'],
    ['Volvo XC60', 5, 5, 'manual', 'suv', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.motortrend.com/uploads/sites/10/2019/08/2020-volvo-xc60-t5-momentum-4wd-suv-angular-front.png'],
    ['Citroen C4', 5, 5, 'manual', 'suv', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.citroen.pt/content/dam/citroen/master/b2c/models/new-c4-e/visualizer/front-view/New%20E-C4%20and%20C4_0MP00NWP_Blanc%20Banquise_FR_1280_720.png'],
    ['Hyundai Tucson', 5, 5, 'manual', 'suv', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.motortrend.com/uploads/sites/10/2019/11/2020-hyundai-tucson-sel-4wd-suv-angular-front.png'],
    ['Toyota Corolla', 5, 5, 'manual', 'sedan', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.toyotaotis.com.ph/wp-content/uploads/2017/04/Altis-Page-Home-image.png'],
    ['Renault Talisman', 5, 5, 'manual', 'sedan', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.chabe.com/wp-content/uploads/2020/06/Renault_Talisman.png'],
    ['Peugeout 508', 5, 5, 'manual', 'sedan', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.pngmart.com/files/22/Peugeot-508-PNG-Image.png'],
    ['Hyundai Ioniq 6', 5, 5, 'manual', 'sedan', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://www.motortrend.com/uploads/sites/10/2019/08/2020-ford-fusion-se-sedan-angular-front.png'],
    ['DS 9', 5, 5, 'manual', 'sedan', 'silver', True, 60, '2024-01-01', '2024-02-01', 'https://cdn.imagin.studio/getImage?customer=robinsandday&make=ds&modelFamily=ds9&modelRange=ds9&modelVariant=od&modelYear=2023&zoomType=fullscreen&steering=right&width=800&angle=01&paintId=pspc0165&fileType=png'],

    # economic
    ['Opel Astra', 5, 5, 'manual', 'sedan', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://www.pngmart.com/files/22/Opel-Astra-Transparent-PNG.png'],
    ['Seat Toledo', 5, 5, 'manual', 'sedan', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://www.seat.gr/content/dam/public/seat-website/models/toledo/specs/versions/seat-toledo-reference.png'],
    ['Fiat Tipo', 5, 5, 'manual', 'sedan', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://www.fiat.pt/content/dam/fiat/cross/models/tipo_2020/opening/desktop/figurini/hatchback/city-life/Tipo-Model-page-MaestroGrey-Car_Desktop-680x430.png'],
    ['Ford Fiesta', 3, 5, 'manual', 'sedan', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://pngimg.com/d/ford_PNG12240.png'],
    ['Renault Megane', 5, 5, 'manual', 'sedan', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://www.sflife.pt/fileuploads/Frotas/M%C3%89DIO%20STATION%20WAGON/_Renault%20Megane%20SW-%20GT%20LINE.png'],
    ['Opel Corsa', 2, 2, 'manual', 'compact', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://www.ab4rent.com/wp-content/uploads/2021/11/CORSA-IMAGEM-SITE.png'],
    ['Seat Ibiza', 2, 2, 'manual', 'compact', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://pngimg.com/d/seat_PNG11814.png'],
    ['Fiat Cronos', 5, 5, 'manual', 'compact', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://portaldoscarros.com.br/wp-content/uploads/2022/10/cronos.png'],
    ['Ford Mondeo', 5, 5, 'manual', 'compact', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://purepng.com/public/uploads/large/purepng.com-ford-mondeo-red-carcarvehicletransportford-961524638418lugc0.png'],
    ['Renault Clio', 5, 5, 'manual', 'compact', 'economic', True, 20, '2024-01-01', '2024-02-01', 'https://purepng.com/public/uploads/large/purepng.com-renaultrenaultfrenchautomobilerenault-cars-and-vansrenaul-trucks-1701527597108vqjil.png'],

]
########## COLOCAR DATA DE REVISÃO E LEGALIZAÇÃO ######################



# Criando as colunas da tabela_carros 'cars'
cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE_CARS}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'name VARCHAR(80) UNIQUE NOT NULL, '
    'doors INTEGER NOT NULL, '
    'seats INTEGER NOT NULL, '
    'gear VARCHAR(80) NOT NULL, '
    'vehicle_type VARCHAR(80) NOT NULL, '
    'category VARCHAR(80) NOT NULL, '
    'available BOOLEAN NOT NULL, '
    'daily_value INTEGER NOT NULL, '
    'legalization_date VARCHAR(80) NOT NULL, '
    'revision_date VARCHAR(80) NOT NULL, '
    'url_images VARCHAR(1000) NOT NULL'
    ')'
)

connection.commit()


# Inserindo dados a tabela_carros 'cars'
sql_cars = (f'INSERT INTO {TABLE_CARS}'
       '(name, doors, seats, gear, vehicle_type, category, available, daily_value, legalization_date, revision_date, url_images) '
       'VALUES '
       '(:name, :doors, :seats, :gear, :vehicle_type, :category, :available, :daily_value, :legalization_date, :revision_date, :url_images)'
            )

# Exceção para evitar dados repetidos
try:
    for data in cars_data:
        cursor.execute(sql_cars, data)

        connection.commit()
except sqlite3.IntegrityError:
    pass


# Dados da tabela_carros 'motorcycles'

motorcycles_data = [
    # gold
    ['Kawasaki Ninja H2R', 998, 228,'sport', 'motorcycle', 'gold', True, 90, '2024-01-01', '2024-02-01', 'https://storage.kawasaki.eu/public/kawasaki.eu/en-EU/model/19ZX1000Y_201GY3DRS1CG_A.png'],
    ['Honda Gold Wing Tour', 1833, 93, 'touring', 'motorcycle', 'gold', True, 90, '2024-01-01', '2024-02-01', 'https://as.sobrenet.pt/s/image/tsr/brandm/product/1920x1280/mc5kyduuta5wawiwh4yejjpxty3.png'],
    ['MV Agusta Rush 1000', 998, 153, 'naked', 'motorcycle', 'gold', True, 90, '2024-01-01', '2024-02-01', 'https://as.sobrenet.pt/s/image/tsr/brandm/product/1920x1280/urwax3aezdzuaflaqfu3kekhwm3.png'],
    ['Harley Davidson Iron 883', 883, 37, 'custom', 'motorcycle', 'gold', True, 90, '2024-01-01', '2024-02-01', 'https://i.pinimg.com/originals/e3/ed/02/e3ed020e17ae3e3cef65f4c92b1ada40.png'],
    ['BMW R18', 1802, 67, 'custom', 'motorcycle', 'gold', True, 90, '2024-01-01', '2024-02-01', 'https://bmwriomotorrad.com.br/storage/app/uploads/public/630/fb5/358/630fb5358127c702778778.png'],

    # silver
    ['Kawasaki Ninja 300', 296, 29, 'sport', 'motorcycle', 'silver', True, 50, '2024-01-01', '2024-02-01', 'https://storage.kawasaki.eu/public/kawasaki.eu/en-EU/Ninja-300-Performance-2016.png'],
    ['Yamaha YZF-R3', 321, 31 , 'sport', 'motorcycle', 'silver', True, 50, '2024-01-01', '2024-02-01', 'https://cdn.riderly.com/storage/media/img/bikes/Yamaha__Yzf-R3.png'],
    ['Ktm Duke 390', 373, 32 , 'naked', 'motorcycle', 'silver', True, 50, '2024-01-01', '2024-02-01', 'https://purepng.com/public/uploads/large/purepng.com-ktm-390-dukemotorcyclemotorbikebikevehiclektm-981525161911xonag.png'],
    ['Honda Forza 300', 279, 18.5 , 'scooter', 'motorcycle', 'silver', True, 50, '2024-01-01', '2024-02-01', 'https://as.sobrenet.pt/s/image/tsr/brandm/product/1920x1280/lfcmzqr2wfuz0bqn43j4rtgcne3.png'],
    ['Harley Davidson Nightster', 975, 66 , 'custom', 'motorcycle', 'silver', True, 50, '2024-01-01', '2024-02-01', 'https://d2bywgumb0o70j.cloudfront.net/2022/04/13/f1f14e0b095004de8e7420f1800d9b07_31edf88d348a73c3.png'],

    # economic
    ['Brixton Cromwell', 125, 8.2, 'naked', 'motorcycle', 'economic', True, 10, '2024-01-01', '2024-02-01', 'https://paultan.org/image/2021/08/2021-Brixton-Motorcycles-BX150-Dark-Green-Malaysia-3.png'],
    ['Keeway RKF', 125, 9.4, 'naked', 'motorcycle', 'economic', True, 10, '2024-01-01', '2024-02-01', 'https://414c561cc1380986c729-8352776009a52c22e7a57d17eef423ea.ssl.cf6.rackcdn.com/motorcycles/rkf%20125%20E5/white/1400*1000%20copy.png'],
    ['Honda PCX', 125, 9.2, 'scooter', 'motorcycle', 'economic', True, 10, '2024-01-01', '2024-02-01', 'https://s2-autoesporte.glbimg.com/hitIiVE1rZAP6jAjc0dgHLV8b_M=/0x0:620x413/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_cf9d035bf26b4646b105bd958f32089d/internal_photos/bs/2020/C/c/AtRksLQ9i42J4ZBToclQ/2019-01-22-pcx-sport-3.4-fd.png'],
    ['Honda CB125R', 125, 11, 'naked', 'motorcycle', 'economic', True, 10, '2024-01-01', '2024-02-01', 'https://as.sobrenet.pt/s/image/tsr/brandm/product/1920x1280/4vr1nrz3x3u3qhmejhumlqrjay3.png'],
    ['Yamaha Fazer', 150, 9.1, 'naked', 'motorcycle', 'economic', True, 10, '2024-01-01', '2024-02-01', 'https://mlfiglnuxfgt.i.optimole.com/RJvaaXw-_n08FBcg/w:382/h:254/q:auto/https://dvrmotosyamaha.com.br/wp-content/uploads/2019/05/fazer-150-azul.png'],
]


# Criando as colunas da tabela_motos 'motorcycles'
cursor.execute(
    f'CREATE TABLE IF NOT EXISTS {TABLE_MOTORCYCLES}'
    '('
    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'name VARCHAR(80) UNIQUE NOT NULL, '
    'cc INTEGER NOT NULL, '
    'powerKW FLOAT NOT NULL, '
    'motorcycle_type VARCHAR(80) NOT NULL, '
    'vehicle_type VARCHAR(80) NOT NULL, '
    'category VARCHAR(80) NOT NULL, '
    'available BOOLEAN NOT NULL, '
    'daily_value INTEGER NOT NULL, '
    'legalization_date VARCHAR(80) NOT NULL, '
    'revision_date VARCHAR(80) NOT NULL, '
    'url_images VARCHAR(1000) '
    ')'
)

connection.commit()

# Inserindo os dados a tabela_motos 'motorcycles'
sql_motorcycles = (f'INSERT INTO {TABLE_MOTORCYCLES}'
       '(name, cc, powerKW, motorcycle_type, vehicle_type, category, available, daily_value, legalization_date, revision_date, url_images) '
       'VALUES '
       '(:name, :cc, :powerKW, :motorcycle_type, :vehicle_type, :category, :available, :daily_value, :legalization_date, :revision_date, :url_images)'
)

# Exceção para evitar dados repetidos
try:
    for data in motorcycles_data:
        cursor.execute(sql_motorcycles, data)

        connection.commit()
except sqlite3.IntegrityError:
    pass


def unavailable_vehicle(table, name):
    # Tornar um veiculo indisponivel

    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor_def = conn.cursor()

    for value in table:

        if value[1] == name:

            if value[5] == "motorcycle":

                cursor_def.execute(
                    f'UPDATE {TABLE_MOTORCYCLES} '
                    'SET available=0 '
                    f'WHERE name="{name}"'
                )
                conn.commit()

            else:

                cursor_def.execute(
                    f'UPDATE {TABLE_CARS} '
                    'SET available=0 '
                    f'WHERE name="{name}"'
                )
                conn.commit()


def available_vehicle(table, name):
    # Tornar um veiculo disponivel

    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor_def = conn.cursor()

    for value in table:

        if value[1] == name:

            if value[5] == "motorcycle":

                cursor_def.execute(
                    f'UPDATE {TABLE_MOTORCYCLES} '
                    'SET available=1 '
                    f'WHERE name="{name}"'
                )
                conn.commit()

            else:

                cursor_def.execute(
                    f'UPDATE {TABLE_CARS} '
                    'SET available=1 '
                    f'WHERE name="{name}"'
                )
                conn.commit()


def get_car():
    # Tabela com apenas os carros

    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor_def = conn.cursor()

    car_table = cursor_def.execute(f"SELECT * FROM {TABLE_CARS}")

    table_car = []
    for row in car_table:
        table_car.append(row)

    return table_car


def get_motorcycle():
    # Uma tabela com apenas as motos

    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor_def = conn.cursor()

    moto_table = cursor_def.execute(f"SELECT * FROM {TABLE_MOTORCYCLES}")

    table_motorcycle = []
    for row in moto_table:
        table_motorcycle.append(row)

    return table_motorcycle

def get_all_vehicles():
    # Uma tabela com todos os veiculos

    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor_def = conn.cursor()
    all_table = []


    table_car = cursor_def.execute(f"SELECT * FROM {TABLE_CARS}")

    for row in table_car:
        all_table.append(row)


    table_moto = cursor_def.execute(f"SELECT * FROM {TABLE_MOTORCYCLES}")

    for row in table_moto:
        all_table.append(row)

    return all_table


def check_vehicle(vehicle_name):
    # função que verifica se o veiculo está disponivel para ser alugado

    table = get_all_vehicles()

    for value in table:

        if value[1] == vehicle_name:

            print(value[7])
            return value[7]


def get_price_vehicle(name_vehicle):

    list_vehicles = get_all_vehicles()

    price = None

    for value in list_vehicles:
        if value[1] == name_vehicle:
            price = value[8]

    return price


def filter_app(table, category_filter=False, vehicles_filter=False, seats_filter=False, price_filter=False, days=False):
    # função para fazer os filtros na app
    # retornando dados requeridos pelo filtro


    new_table = []

    for value in table:

        # categoria
        if category_filter and not vehicles_filter and not seats_filter and not price_filter:
            if value[6] in category_filter:
                new_table.append(value)

        # veiculo
        elif vehicles_filter and not category_filter and not seats_filter and not price_filter:
            if value[5] in vehicles_filter:
                new_table.append(value)

        # assentos
        elif seats_filter and not category_filter and not vehicles_filter and not price_filter:
            if value[3] in seats_filter:
                new_table.append(value)

        # preço
        elif price_filter and not category_filter and not vehicles_filter and not seats_filter:
            daily_price = int(value[8]) * int(days)
            new_value = check_price(price_filter, daily_price, value)
            if new_value is not None:
                new_table.append(new_value)

        # categoria, veiculos
        elif category_filter and vehicles_filter and not seats_filter and not price_filter:
            if value[6] in category_filter and value[5] in vehicles_filter:
                new_table.append(value)

        # categoria, assentos
        elif category_filter and seats_filter and not vehicles_filter and not price_filter:
            if value[6] in category_filter and value[3] in seats_filter:
                new_table.append(value)

        # categoria, preços
        elif category_filter and price_filter and not vehicles_filter and not seats_filter:
            daily_price = int(value[8]) * int(days)
            if value[6] in category_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # assentos, veiculos
        elif seats_filter and vehicles_filter and not category_filter and not price_filter:
            if value[3] in seats_filter and value[5] in vehicles_filter:
                new_table.append(value)

        # assentos, preços
        elif seats_filter and price_filter and not category_filter and not vehicles_filter:
            daily_price = int(value[8]) * int(days)
            if value[3] in seats_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # preços, veiculos
        elif vehicles_filter and price_filter and not category_filter and not seats_filter:
            daily_price = int(value[8]) * int(days)
            if value[5] in vehicles_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # categoria, veiculos, assentos
        elif category_filter and vehicles_filter and seats_filter and not price_filter:
            if value[6] in category_filter and value[3] in seats_filter \
                        and value[5] in vehicles_filter:
                new_table.append(value)

        # preço, categoria, veiculo
        elif price_filter and category_filter and vehicles_filter and not seats_filter:
            daily_price = int(value[8]) * int(days)

            if value[6] in category_filter and value[5] in vehicles_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # assentos, preço, categoria
        elif seats_filter and price_filter and category_filter and not vehicles_filter:
            daily_price = int(value[8]) * int(days)
            if value[3] in seats_filter and value[6] in category_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # veiculo, assento, preço
        elif vehicles_filter and seats_filter and price_filter and not category_filter:
            daily_price = int(value[8]) * int(days)
            if value[5] in vehicles_filter and value[3] in seats_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

        # veiculo, assento, categoria, preço
        elif vehicles_filter and seats_filter and price_filter and category_filter:
            daily_price = int(value[8]) * int(days)
            if value[3] in seats_filter and value[5] in vehicles_filter and value[6] in category_filter:
                new_value = check_price(price_filter, daily_price, value)
                if new_value is not None:
                    new_table.append(new_value)

    return new_table


def check_price(price_filter, price, value):
    # função que irá filtrar o 'daily_price' que no qual foi pedido

    if price_filter > 200:
        if price > price_filter:
            return value

    else:
        if price <= price_filter:
            return value


cursor.close()
connection.close()

if __name__ == "__main__":

    ...