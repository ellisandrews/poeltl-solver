import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .common import CONFERENCES, RAW_DATA_DIRECTORY, slugify
from ..db.models import Base, Conference, Division, Player, Team


DIVISION_ABBREVIATIONS = {
    'Atlantic': 'Atl.',
    'Central': 'Cen.',
    'Northwest': 'NW',
    'Pacific': 'Pac.',
    'Southeast': 'SE',
    'Southwest': 'SW'
}


def get_height_inches(raw_player):
    try:
        feet = int(raw_player['height']['feets'])
        inches = int(raw_player['height']['inches'])
        return feet * 12 + inches
    except:
        return None


if __name__ == '__main__':

    # NOTE: This assumes `CREATE DATABASE poeltl;` has already been run manually

    # TODO: Extract db config
    engine = create_engine('postgresql://postgres@localhost/poeltl', echo=True)
    
    # Create all tables
    Base.metadata.create_all(engine)

    # Create a database session to which we'll add objects
    session = Session(engine)

    # First, create conferences/divisions/teams from conference data.
    for conference_name in CONFERENCES:
        
        conference = Conference(name=conference_name)
        session.add(conference)

        with open(f"{RAW_DATA_DIRECTORY}/teams_{slugify(conference_name)}.json", 'r') as raw_teams_file:
            raw_teams = json.load(raw_teams_file)

        # TODO: DELETE THIS LINE AS IT'S NOW UPSTREAM IN DATA FETCHING
        raw_teams = [raw_team for raw_team in raw_teams if (not raw_team['allStar'] and raw_team['nbaFranchise'])]

        for raw_team in raw_teams:

            division_name = raw_team['leagues']['standard']['division']
            
            division = session.query(Division).filter_by(name=division_name).one_or_none()
            if not division:
                division = Division(
                    name=division_name,
                    abbreviation=DIVISION_ABBREVIATIONS[division_name],
                    conference=conference
                )
                session.add(division)
            
            team = Team(
                id=raw_team['id'],
                city=raw_team['city'],
                nickname=raw_team['nickname'],
                code=raw_team['code'],
                division=division
            )
            session.add(team)

    # Next, create players from team player lists
    for team in session.query(Team).all():
        
        # TODO: CHANGE THIS ONCE FILES HAVE IDs?
        with open(f"{RAW_DATA_DIRECTORY}/players_{slugify(team.city + ' ' + team.nickname)}.json", 'r') as raw_players_file:
             raw_players = json.load(raw_players_file)           

        # TODO: DELETE THIS LINE AS IT'S NOW UPSTREAM IN DATA FETCHING
        raw_players = [raw_player for raw_player in raw_players if (raw_player['leagues'].get('standard') and raw_player['leagues']['standard']['active'])]

        for raw_player in raw_players:
            player = Player(
                first_name=raw_player['firstname'],
                last_name=raw_player['lastname'],
                birth_date=raw_player['birth']['date'],
                height_inches=get_height_inches(raw_player),
                jersey_number=raw_player['leagues']['standard']['jersey'] or 0,  # Players with number 0 show up as null, so just going to overcorrect this
                position=raw_player['leagues']['standard']['pos'],
                team=team
            )
            session.add(player)

            # Note: Not enforcing uniqueness on player as there is some bad data in the API.
            # Example of this is Justin Anderson existing 3 times in the raw data on different teams:
            # SELECT * FROM players p JOIN teams t ON p.team_id = t.id WHERE first_name = 'Justin' and last_name = 'Anderson';

    session.commit()
    session.close()
