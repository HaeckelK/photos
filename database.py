import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import UniqueConstraint


Base = declarative_base()


class Database:
    # engine = create_engine('sqlite:///:memory:', echo=True)
    engine = create_engine('sqlite:///test.db', echo=True)

    def __init__(self) -> None:
        Session = sessionmaker(bind=Database().engine)
        return

    def add_photo(self) -> None:
        session = self.Session()
        session.close()
        return


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow)


class Photo(Base, TimestampMixin):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    source = Column(String)
    filename = Column(String)

    __table_args__ = (UniqueConstraint('source', 'filename', name='_source_filename_uc'),
                     )


class Thumbnail(Base, TimestampMixin):
    __tablename__ = 'thumbnail'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    height = Column(Integer)
    width = Column(Integer)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship('Photo')


class PhotoCategory(Base, TimestampMixin):
    __tablename__ = "photo_category"

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship('Photo')


class PhotoTag(Base, TimestampMixin):
    __tablename__ = "photo_tag"

    id = Column(Integer, primary_key=True)
    tag = Column(String)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship('Photo')


class PhotoNote(Base, TimestampMixin):
    __tablename__ = "photo_note"

    id = Column(Integer, primary_key=True)
    note = Column(String)
    photo_id = Column(Integer, ForeignKey('photo.id'))
    photo = relationship('Photo')


Base.metadata.create_all(Database.engine)
# Session = sessionmaker(bind=Database().engine)
# session = Session()

# photo = Photo(source="sandbox", filename="abc.jpg")
# session.add(photo)

# thumb = Thumbnail(filename="tn_abc.jpg", height=999, width=999, photo=photo)
# session.add(thumb)


# session.add(PhotoTag(tag="snow", photo=photo))
# session.add(PhotoTag(tag="xmas", photo=photo))

# session.add(PhotoNote(note="First Xmas in the new house.", photo=photo))

# session.commit()

# for instance in session.query(Photo).order_by(Photo.id):
#     print(instance.id, instance.source, instance.filename)

# session.close()