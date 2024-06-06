from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    com_hostname = StringField("Nom de l'ordinateur", validators=[
        Length(min=2, max=255, message="La longueur doit être entre 2 et 255 caractères"),
        DataRequired("Ce champ est requis")
    ])
    com_ip_address = StringField("Adresse IP de l'ordinateur", validators=[
        Length(min=2, max=15, message="La longueur doit être entre 2 et 15 caractères"),
        DataRequired("Ce champ est requis")
    ])
    com_os = StringField("Système d'exploitation", validators=[
        Length(min=2, max=255, message="La longueur doit être entre 2 et 255 caractères"),
        DataRequired("Ce champ est requis")
    ])
    com_processor = StringField("Processeur", validators=[
        Length(min=2, max=255, message="La longueur doit être entre 2 et 255 caractères"),
        DataRequired("Ce champ est requis")
    ])
    com_ram = StringField("RAM", validators=[
        DataRequired("Ce champ est requis")
    ])
    submit = SubmitField("Enregistrer ordinateur")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_genre_update_wtf = StringField("Clavioter le genre ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteComputer(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_computer_delete_wtf = StringField("Effacer ce computer", render_kw={'readonly': True})
    submit_btn_del = SubmitField("Effacer computer")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
