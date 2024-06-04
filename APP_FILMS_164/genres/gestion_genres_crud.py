"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect, request, session, url_for, render_template, flash
from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres, FormWTFDeleteComputer, \
    FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /computers_afficher

    Test : ex : http://127.0.0.1:5575/computers_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_computer_sel = 0 >> tous les ordinateurs.
                id_computer_sel = "n" affiche l'ordinateur dont l'id est "n"
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
                    valeur_id_computer_selected_dictionnaire = {"value_id_computer_selected": id_computer_sel}
                    strsql_computers_afficher = """SELECT * FROM t_computer WHERE idComputer = %(value_id_computer_selected)s"""
                    mc_afficher.execute(strsql_computers_afficher, valeur_id_computer_selected_dictionnaire)
                else:
                    strsql_computers_afficher = """SELECT * FROM t_computer ORDER BY idComputer DESC"""
                    mc_afficher.execute(strsql_computers_afficher)

                data_computers = mc_afficher.fetchall()

                print("data_computers ", data_computers, " Type : ", type(data_computers))

                if not data_computers and id_computer_sel == 0:
                    flash("""La table "t_computer" est vide. !!""", "warning")
                elif not data_computers and id_computer_sel > 0:
                    flash(f"Aucun ordinateur trouvé !!", "warning")
                else:
                    flash(f"Données des ordinateurs affichées !!", "success")

        except Exception as Exception_computers_afficher:
            raise ExceptionComputersAfficher(f"fichier : {Path(__file__).name}  ;  "
                                             f"{computers_afficher.__name__} ; "
                                             f"{Exception_computers_afficher}")

    return render_template("computers/computers_afficher.html", data=data_computers)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5575/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_genre": name_genre}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_genre (id_genre,intitule_genre) VALUES (NULL,%(value_intitule_genre)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("genres/genres_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    id_genre_update = request.values['id_genre_btn_edit_html']
    form_update = FormWTFUpdateGenre()
    try:
        if request.method == "POST" and form_update.submit.data:
            name_genre_update = form_update.nom_genre_update_wtf.data.lower()
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_name_genre": name_genre_update,
                                          "value_date_genre_essai": date_genre_essai}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_genre SET intitule_genre = %(value_name_genre)s, 
                                              date_ins_genre = %(value_date_genre_essai)s WHERE id_genre = %(value_id_genre)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))
        elif request.method == "GET":
            str_sql_id_genre = "SELECT id_genre, intitule_genre, date_ins_genre FROM t_genre WHERE id_genre = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["intitule_genre"])

            form_update.nom_genre_update_wtf.data = data_nom_genre["intitule_genre"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["date_ins_genre"]

    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /computer_delete

    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
"""


@app.route("/computer_delete", methods=['GET', 'POST'])
def computers_delete_wtf():
    data_notes_attribue_computer_delete = None
    btn_submit_del = None
    id_computer_delete = request.values['id_computer_btn_delete_html']
    form_delete = FormWTFDeleteComputer()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("computers_afficher", order_by="ASC", id_computer_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_notes_attribue_computer_delete = session['data_notes_attribue_computer_delete']
                print("data_notes_attribue_computer_delete ", data_notes_attribue_computer_delete)

                flash(f"Effacer l'ordinateur de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_computer": id_computer_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_idcomputer = """DELETE FROM t_computer WHERE idComputer = %(value_id_computer)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_idcomputer, valeur_delete_dictionnaire)

                flash(f"Ordinateur définitivement effacé !!", "success")
                print(f"Ordinateur définitivement effacé !!")

                return redirect(url_for('computers_afficher', order_by="ASC", id_computer_sel=0))

    if request.method == "GET":
        valeur_select_dictionnaire = {"value_id_computer": id_computer_delete}
        print(id_computer_delete, type(id_computer_delete))

        # Sélectionner l'ordinateur spécifique à supprimer
        str_sql_id_computer = "SELECT * FROM t_computer WHERE idComputer = %(value_id_computer)s"
        with DBconnection() as mydb_conn:
            mydb_conn.execute(str_sql_id_computer, valeur_select_dictionnaire)
            data_nom_computer = mydb_conn.fetchone()
            print("data_nom_computer ", data_nom_computer, " type ", type(data_nom_computer))

            # Vérifie si la clé 'computerName' existe dans le dictionnaire avant de l'utiliser
            if data_nom_computer and 'computerName' in data_nom_computer:
                form_delete.nom_computer_delete_wtf.data = data_nom_computer["computerName"]
            else:
                # Gérer le cas où la clé 'computerName' n'existe pas dans le dictionnaire
                # ou si le dictionnaire est vide
                form_delete.nom_computer_delete_wtf.data = "Nom de l'ordinateur non disponible"

        btn_submit_del = False

