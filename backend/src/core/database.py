from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
db_session = scoped_session(sessionmaker())
engine = None

def init_db(app):
    global engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URL_APP'])
    db_session.configure(bind=engine)
    Base.metadata.bind = engine
    
    # Importez tous les modèles ici pour que SQLAlchemy les connaisse
    from  backend.src.users.models import User
    from  backend.src.campaigns.database import Campaign
    from  backend.src.relations.user_campaign import setup_relationships
    
    setup_relationships()
    Base.metadata.create_all(bind=engine)