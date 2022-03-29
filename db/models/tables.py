from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table


metadata = MetaData()


conferences = Table(
    'conferences',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(10), nullable=False)
)


divisions = Table(
    'divisions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('abbreviation', String(10), nullable=False),
    Column('conference_id', Integer, ForeignKey('conferences.id'), nullable=False)
)


teams = Table(
    'teams',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('city', String(50), nullable=False),
    Column('nickname', String(50), nullable=False),
    Column('code', String(10), nullable=False),
    Column('division_id', Integer, ForeignKey('divisions.id'), nullable=False)
)


players = Table(
    'players',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('birth_date', Date, nullable=False),
    Column('height_inches', Integer, nullable=False),
    Column('jersey_number', Integer, nullable=False),
    Column('position', String(10), nullable=False),
    Column('team_id', Integer, ForeignKey('teams.id'), nullable=False)
)
