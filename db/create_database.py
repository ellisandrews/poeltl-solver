from curses import echo, raw
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, Conference, Division, Player, Team


EXCLUDED_TEAM_CODES = set([
    ''
])



if __name__ == '__main__':

    # NOTE: This assumes `CREATE DATABASE poeltl;` has already been run manually

    # TODO: Extract db config
    engine = create_engine('postgresql://postgres@localhost/poeltl', echo=True)
    
    # Create all tables
    Base.metadata.create_all(engine)

    session = Session(engine)

    for conference_name in ('East', 'West'):
        
        conference = Conference(name=conference_name)
        session.add(conference)

        with open(f"db/data/raw/teams_{conference_name.lower()}.json", 'r') as raw_teams_file:
            raw_teams = json.load(raw_teams_file)

        divisions_by_name = {}

        for raw_team in raw_teams:

            # Only want NBA teams
            if raw_team['allStar'] or not raw_team['nbaFranchise']:
                continue

            division_name = raw_team['leagues']['standard']['division']
            
            if division_name not in divisions_by_name:
                division = Division(name=division_name, conference=conference)
                session.add(division)
                divisions_by_name[division_name] = division
            else:
                division = divisions_by_name[division_name]

            team = Team(
                id=raw_team['id'],
                city=raw_team['city'],
                nickname=raw_team['nickname'],
                code=raw_team['code'],
                division=division
            )
            session.add(team)

    session.commit()
    session.close()
