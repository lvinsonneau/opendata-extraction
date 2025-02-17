from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db




class Publication(db.Model):
    __tablename__ = 'publication'
    id: int = db.Column(db.Integer, primary_key=True)
    numero_de_lacte: str = db.Column(db.String(20), nullable=False)
    objet: str = db.Column(db.String(256), nullable=False)
    siren: str = db.Column(db.String(9), nullable=False)
    # 0:oui, 1:non, 2:ne sais pas
    publication_open_data: str = db.Column(db.String(1), nullable=False, server_default='0')
    date_de_lacte: str = db.Column(db.DateTime(), nullable=False)
    classification_code = db.Column(db.String(10), nullable=False)
    classification_nom = db.Column(db.String(100), nullable=False)
    acte_nature: str = db.Column(db.String(50), nullable=False)
    envoi_depot: str = db.Column(db.String(50), nullable=False)
    # utilise pour les budget
    date_budget = db.Column(db.String(10), nullable=True)
    est_masque = db.Column('est_masque', db.Boolean(), nullable=False, server_default='0')
    # 1 => publie, 0:non, 2:en-cours,3:en-erreur
    etat: str = db.Column('etat', db.String(1), nullable=False, server_default='0')
    created_at: str = db.Column(db.DateTime(), nullable=False)
    modified_at: str = db.Column(db.DateTime(), nullable=False)
    actes = relationship("Acte", lazy="joined")
    pieces_jointe = relationship("PieceJointe", lazy="joined")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'numero_de_lacte': self.numero_de_lacte,
            'objet': self.objet,
            'siren': self.siren,
            'publication_open_data': self.publication_open_data,
            'etat': self.etat,
            'date_budget': self.date_budget,
            'est_masque': self.est_masque,
            'date_de_lacte': self.date_de_lacte,
            'classification_code': self.classification_code,
            'classification_nom': self.classification_nom,
            'acte_nature': self.acte_nature,
            'actes': [item.serialize for item in self.actes],
            'pieces_jointe': [item.serialize for item in self.pieces_jointe]
        }

    @property
    def serialize_many2many(self):
        return [item.serialize for item in self.many2many]


class Acte(db.Model):
    __tablename__ = 'acte'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False)
    url: str = db.Column(db.String(500), nullable=False)
    # ajout du path pour la task publier_acte_task (utiliser en backend)
    path: str = db.Column(db.String(500), nullable=False)
    publication_id = Column(Integer, ForeignKey('publication.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'path': self.path,
            'publication_id': self.publication_id
        }


class PieceJointe(db.Model):
    __tablename__ = 'pj_acte'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(200), nullable=False)
    url: str = db.Column(db.String(500), nullable=False)
    # ajout du path pour la task publier_acte_task (utiliser en backend)
    path: str = db.Column(db.String(500), nullable=False)
    publication_id = Column(Integer, ForeignKey('publication.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'path': self.path,
            'publication_id': self.publication_id
        }
