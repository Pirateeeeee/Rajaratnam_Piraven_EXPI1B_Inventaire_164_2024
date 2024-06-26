"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteComputer
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher

    Test : ex : http://127.0.0.1:5575/computers_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/computers_afficher/<string:order_by>/<int:id_computer_sel>", methods=['GET', 'POST'])
def computers_afficher(order_by, id_computer_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_computer_sel == 0:
                    strsql_computers_afficher = """SELECT * FROM t_computer ORDER BY idComputer ASC"""
                    mc_afficher.execute(strsql_computers_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable

                    valeur_id_computer_selected_dictionnaire = {"value_id_computer_selected": id_computer_sel}
                    strsql_computers_afficher = """SELECT * FROM t_computer WHERE idComputer = %(value_id_computer_selected)s"""

                    mc_afficher.execute(strsql_computers_afficher, valeur_id_computer_selected_dictionnaire)
                else:
                    strsql_computers_afficher = """SELECT *  FROM t_computer ORDER BY idComputer DESC"""

                    mc_afficher.execute(strsql_computers_afficher)

                data_computers = mc_afficher.fetchall()

                print("data_computers ", data_computers, " Type : ", type(data_computers))

                # Différencier les messages si la table est vide.
                if not data_computers and id_computer_sel == 0:
                    flash("""La table "t_genre" est vide. !!""", "warning")
                elif not data_computers and id_computer_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Aucun ordinateur n'a été trouvé !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données des ordinateurs affichés !!", "success")

        except Exception as Exception_computers_afficher:
            raise ExceptionComputersAfficher(f"fichier : {Path(__file__).name}  ;  "
                                             f"{computers_afficher.__name__} ; "
                                             f"{Exception_computers_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/genre_afficher.html", data=data_computers)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5575/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                com_computer_wtf = form.com_hostname.data
                com_computer = com_computer_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_comHostname": com_computer}
                print('valeurs_insertion_dictionnaire', valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_computer (idComputer, comHostname) VALUES (NULL,%(value_comHostname)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("genres/genre_ajouter_wtf.html", form=form)





"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    id_genre_update = request.values['id_genre_btn_edit_html']
    form_update = FormWTFUpdateGenre()
    try:
        if request.method == "POST" and form_update.submit.data:
            name_genre_update = form_update.nom_genre_update_wtf.data
            name_genre_update = name_genre_update.lower()
            description_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_name_genre": name_genre_update,
                                          "value_description_genre_essai": description_genre_essai}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_computer SET nom_c = %(value_name_genre)s, 
            description_c = %(value_description_genre_essai)s WHERE id_computer = %(value_id_genre)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))
        elif request.method == "GET":
            str_sql_id_genre = "SELECT id_computer, nom_c, description_c FROM t_computer WHERE id_computer = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ", data_nom_genre["nom_c"])

            form_update.nom_genre_update_wtf.data = data_nom_genre["nom_c"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["description_c"]

    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)

@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    id_genre_delete = request.values['id_genre_btn_delete_html']
    form_delete = FormWTFDeleteComputer()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)
                flash(f"Effacer le Computer de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_computer WHERE id_computer = %(value_id_genre)s"""
                str_sql_delete_idgenre = """DELETE FROM t_computer WHERE id_computer = %(value_id_genre)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Computer définitivement effacée !!", "success")
                print(f"Computer définitivement effacée !!")
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            str_sql_genres_films_delete = """SELECT id_computer, nom_m, id_computer, nom_c FROM t_computer 
                                            INNER JOIN t_computer ON t_computer.id_computer = t_computer.id_computer
                                            WHERE id_computer = %(value_id_genre)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                str_sql_id_genre = "SELECT id_computer, nom_c FROM t_computer WHERE id_computer = %(value_id_genre)s"
                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ", data_nom_genre["nom_c"])

            form_delete.nom_genre_delete_wtf.data = data_nom_genre["nom_c"]
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionComputerDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)

