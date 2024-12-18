from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from app import app, db
from models import (Users, Reservations, PaymentData, filter_app, get_car, get_motorcycle, get_all_vehicles,
                    unavailable_vehicle, available_vehicle, check_vehicle, get_price_vehicle)
from datetime import date, timedelta


# lendo a tabela "cars"
CAR_TABLE = get_car()

# lendo a tabela "motorcycles"
MOTORCYCLE_TABLE = get_motorcycle()

# juntando as tabelas
ALL_VEHICLES = get_all_vehicles()



# Esta será a primeira página a ser carregada
# Pagina onde fará o aluguer do veiculo e também onde se fará o gerenciamento da reserva
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    # Primeiro trataremos do gerencimento

    # Verificando se usuário está logado
    username = None
    if current_user.is_authenticated:
        username = current_user.username

    today = date.today()

    # Variavél que será usada para limitar a antecedência de uma reserva(que será no maximo de 1 ano)
    delta = timedelta(days=366)

    # Obter dados do banco de dados
    user = Reservations.query.all()

    data_list = []

    # Caso o usuário tenha alguma reserva feita, essa reserva será armazenada em listas
    # para melhor tratamento dentro do HTML
    for value in user:

        if username == value.username:
            data_list.append([value.client_name, value.car_name, value.pick_up_date, value.drop_off_date])

    if request.method == "POST":

        # Carro escolhido pelo usuário
        car_name = request.form.get('car-name-management')

        # tratando de possiveis erros que possam ocorrer com relação a data que o usuário colocar
        try:

            # Extraindo dados da rota
            pick_up_date_management = request.form.get("pick-up-date-management")
            drop_off_date_management = request.form.get("drop-off-date-management")

            # Verificando se o usuário enviou a dados
            if pick_up_date_management or drop_off_date_management:

                for value in user:

                    if username == value.username:

                        if pick_up_date_management:
                            # Transformando TODOS os dado enviado pelo usuário ou não numa variavel do tipo 'date'
                            # para tratamento de erros
                            pick_up_date_management = date.fromisoformat(pick_up_date_management)

                        else:
                            pick_up_date_management = date.fromisoformat(value.pick_up_date)

                        if drop_off_date_management:

                            drop_off_date_management = date.fromisoformat(drop_off_date_management)

                        else:
                            drop_off_date_management = date.fromisoformat(value.drop_off_date)

                # Verificando se a data de levantar o veiculo for menor que o dia atual
                if pick_up_date_management < today:
                    flash("Date error: Date cannot be less than the current day", "error")
                    return redirect(url_for("home", data_list=data_list))

                # Se a data de retirada for maior ou igual que a de entrega
                if pick_up_date_management >= drop_off_date_management:
                    flash("Date error: drop off date is incorrect", "error")
                    return redirect(url_for("home", data_list=data_list))

                # Só será permitido reservas até um ano da data atual
                if pick_up_date_management > (today + delta):
                    flash("Date error: Reservations can only be made up to one year", "error")
                    return redirect(url_for("home", data_list=data_list))

                # Nessa parte trataremos dos dados enviados pelo usuário e guarda-los na base de dados
                for value in user:

                    # Igualando o usuário logado com o usuário da base de dados da reserva
                    if username == value.username:

                        # Direcionando o carro escolhido com o carro na base de dados para alterar o dia
                        if car_name == value.car_name:
                            value.pick_up_date = pick_up_date_management
                            value.drop_off_date = drop_off_date_management
                            db.session.commit()
                            return redirect(url_for("home", data_list=data_list))

        except ValueError:
            flash("Date error: Year incorrect", "error")
            return redirect(url_for("home", data_list=data_list))

        # Para cancelar reserva
        if car_name:

            for value in user:

                # Igualando o usuário logado com o usuário da base de dados da reserva
                if username == value.username:

                    # Direcionando o carro escolhido com o carro na base de dados para cancelar reserva
                    if car_name == value.car_name:
                        db.session.delete(value)
                        db.session.commit()
                        available_vehicle(ALL_VEHICLES, value.car_name)
                        flash("Cancellation done successfully", "success")
                        return redirect(url_for("home", data_list=data_list))


    # Daqui trataremos do aluguer do carro
    # Extraindo dados de aluguer da rota
    if request.method == "POST":

        vehicle_type = request.form.get("vehicle-type")

        # No html o usuário pode escolher um ano com 5 ou mais números(Ex: 20.000)
        # Esta exceção é para evitar que isso ocorra

        if vehicle_type:

            try:

                # Extraindo dados da rota
                pick_up_date = date.fromisoformat(request.form.get("pick-up-date"))
                drop_off_date = date.fromisoformat(request.form.get("drop-off-date"))

                # Verificando se a data de levantar o veiculo for menor que o dia atual
                if pick_up_date < today:
                    flash("Date error: Date cannot be less than the current day", "error")
                    return redirect(url_for("home"))

                # Se a data de retirada for maior ou igual que a de entrega
                if pick_up_date >= drop_off_date:
                    flash("Date error: drop off date is incorrect", "error")
                    return redirect(url_for("home"))

                # Só será permitido reservas até um ano da data atual
                if pick_up_date > (today + delta):
                    flash("Date error: Reservations can only be made up to one year", "error")
                    return redirect(url_for("home"))

            except ValueError:
                flash("Date error: Year incorrect", "error")
                return redirect(url_for("home"))

            # Calculando os dias da reserva
            days = drop_off_date - pick_up_date

            # Guardando apenas os dias (int)
            days = days.days

            return redirect(url_for("results", vehicle_type=vehicle_type, pick_up_date=pick_up_date,
                                drop_off_date=drop_off_date, days=days))

    return render_template("home.html", data_list=data_list)


# Pagina que mostrará o resultado da pesquisa para alugar um veiculo
@app.route("/results", methods=["GET", "POST"])
def results():


    # Extraindo dados do URL
    vehicle_type = request.args.get('vehicle_type')
    days = request.args.get('days')
    pick_up_date = request.args.get('pick_up_date')
    drop_off_date = request.args.get('drop_off_date')

    new_table_car = []
    new_table_motorcycle = []
    new_table_all_vehicles = []

    # filtro
    if request.method == "POST":

        # Extraindo dados da rota
        category_filter = request.form.getlist('filter-category')
        vehicles_filter = request.form.getlist('filter-vehicle-type')
        price_filter = request.form.get('filter-price', type=int)
        seats_filter = request.form.getlist('filter-seats', type=int)



        # Condição para caso o usuário NÃO usar o filtro
        # NÃO apareça uma 'flash message'
        # E com isso aparecerá a mensagem de erro apenas se
        # o usuário usar o filtro
        if category_filter or vehicles_filter or seats_filter or price_filter:

            # tabelas filtradas de acordo com o tipo de veiculo requerido pelo cliente
            if vehicle_type == "cars":
                new_table_car = filter_app(CAR_TABLE, category_filter, vehicles_filter, seats_filter, price_filter, days)

            if vehicle_type == "motorcycles":
                new_table_motorcycle = filter_app(MOTORCYCLE_TABLE, category_filter, vehicles_filter, seats_filter, price_filter, days)

            if vehicle_type == "all":
                new_table_all_vehicles = filter_app(ALL_VEHICLES, category_filter, vehicles_filter, seats_filter, price_filter, days)

            # Caso as tabelas retornem nenhum valor
            # Uma flash message irá aparecer indicando que o veiculo não foi encontrado
            if not new_table_car and not new_table_motorcycle and not new_table_all_vehicles:
                flash("vehicle not found", "error")
                return redirect(url_for("results", vehicle_type=vehicle_type, pick_up_date=pick_up_date,
                                        drop_off_date=drop_off_date, days=days))


    # Escolha do carro
    if request.method == "POST":

        # Extraindo dados da rota
        user_vehicle = request.form.get('choose-vehicle')

        # Verificar se o resquest foi feito no template
        if user_vehicle:


            # verificar se o veiculo escolhido está disponivel
            if not check_vehicle(user_vehicle):

                # mensagem de erro caso o veiculo esteja indisponivel
                flash("vehicle unavailable", "error")
                return redirect(url_for("results", vehicle_type=vehicle_type, pick_up_date=pick_up_date,
                                        drop_off_date=drop_off_date, days=days))


            else:
                # verificando se o usuário está logado
                if current_user.is_authenticated:

                    # guardando dados da reserva
                    client_name = f'{current_user.first_name} {current_user.last_name}'


                    return redirect(url_for("payment", client_name=client_name, user_vehicle=user_vehicle,
                                            pick_up_date=pick_up_date, drop_off_date=drop_off_date, days=days))

                else:
                    flash("You need to login", "error")
                    return redirect(url_for("login", vehicle_type=vehicle_type, days=days, pick_up_date=pick_up_date,
                                            drop_off_date=drop_off_date))


    return render_template("results.html", car_table=CAR_TABLE, new_table_car=new_table_car,
                           new_table_motorcycle=new_table_motorcycle, motorcycle_table=MOTORCYCLE_TABLE,
                           vehicle_type=vehicle_type, new_table_all_vehicles=new_table_all_vehicles, days=days)


# Pagamento
# Esta rota só será acessada se o usuário estiver logado
@app.route("/payment", methods=["GET", "POST"])
def payment():

    # Extraindo dados da URL
    client_name = request.args.get('client_name')
    user_vehicle = request.args.get('user_vehicle')
    pick_up_date = request.args.get('pick_up_date')
    drop_off_date = request.args.get('drop_off_date')
    days = request.args.get('days', type=int)

    # Obtendo o valor da diaria do veiculo escolhido pelo usuario
    price_day = get_price_vehicle(user_vehicle)

    if request.method == "POST":

        # Extraindo dados da rota
        card_holder = request.form.get('card-holder')
        email = request.form.get('email')
        card_number = request.form.get('card-number')
        expiration_date = request.form.get('expiration')
        cvc = request.form.get('cvc')

        username = current_user.username

        # Dados da Reserva
        reserve = Reservations(username, client_name, user_vehicle, pick_up_date, drop_off_date, days)

        # guardando dados da reserva na base de dados
        db.session.add(reserve)
        db.session.commit()

        # Dados pagamento
        data = PaymentData(username, card_holder, email, card_number, expiration_date, cvc)

        # guardando dados do pagamento na base de dados
        db.session.add(data)
        db.session.commit()

        # tornar o veiculo escolhido indisponivel
        unavailable_vehicle(ALL_VEHICLES, user_vehicle)

        flash("reservation made successfully", "success")
        return redirect(url_for("home"))



    return render_template("payment.html", client_name=client_name, pick_up_date=pick_up_date, drop_off_date=drop_off_date,
                           days=days, user_vehicle=user_vehicle, price_day=price_day)



# Para o usuário fazer o login ou se registrar
@app.route("/login", methods=["GET", "POST"])
def login():


    # Extraindo dados do URL
    vehicle_type = request.args.get('vehicle_type')
    days = request.args.get('days')
    pick_up_date = request.args.get('pick_up_date')
    drop_off_date = request.args.get('drop_off_date')


    if request.method == "POST":

        # Extraindo dados da rota
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()


        # verifica se o usuario existe ou se a senha esta correta
        # retornando uma mensagem de erro
        if not user or not user.verify_password(password):
            flash("Password or username is incorrect.", "error")
            return redirect(url_for("login", vehicle_type=vehicle_type, days=days, pick_up_date=pick_up_date,
                                    drop_off_date=drop_off_date))

        # estando tudo correto o usuário é logado
        login_user(user)

        # Verificando se o usuário já registrou os dados para fazer o aluguer
        # Assim retorna diretamente a pagina dos resultados para a escolha do carro
        if vehicle_type and days and pick_up_date and drop_off_date:
            return redirect(url_for("results", vehicle_type=vehicle_type, days=days, drop_off_date=drop_off_date,
                                    pick_up_date=pick_up_date))
        else:
            return redirect(url_for("home"))


    return render_template("login.html")


# Página de registro do usuário
@app.route("/register", methods=["GET", "POST"])
def register():


    # Extraindo dados do URL
    vehicle_type = request.args.get('vehicle_type')
    days = request.args.get('days')
    pick_up_date = request.args.get('pick_up_date')
    drop_off_date = request.args.get('drop_off_date')


    if request.method == "POST":

        # Extraindo dados da rota
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")


        # Esta exceção serve apenas para quando o banco de dados estiver vazio
        try:
            check_username = Users.query.filter_by(username=username).first()

            # Se o usuário escolher um nome de usuário que já exista
            # não aceita e retorna a pagina junto com o erro a alertar do mesmo
            if username == check_username.username:
                flash("Username already exists.", "error")
                return redirect(url_for("register"))

        except AttributeError:
            pass


        user = Users(first_name, last_name, username, password)

        # Adicionando os dados ao banco de dados
        db.session.add(user)
        db.session.commit()

        flash("User created successfully", "success")
        return redirect(url_for("login", vehicle_type=vehicle_type, days=days, pick_up_date=pick_up_date,
                                drop_off_date=drop_off_date))

    return render_template("register.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))



if __name__ == "__main__":

    app.run(debug=True)
