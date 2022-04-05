-- Zach Collins (correct query)
SELECT
    players.id,
    players.first_name,
    players.last_name,
    players.birth_date,
    players.height_inches,
    players.jersey_number,
    players.position,
    players.team_id
FROM players JOIN teams ON teams.id = players.team_id 
JOIN divisions ON divisions.id = teams.division_id 
JOIN conferences ON conferences.id = divisions.conference_id
WHERE 
    (teams.code NOT IN ('SAS')) 
AND conferences.name != 'West' 
AND (divisions.abbreviation NOT IN ('SW')) 
AND players.position IN ('C-F', 'F') 
AND players.height_inches IN (81, 82) 
AND date_part('YEAR', age(CURRENT_DATE, players.birth_date)) IN (25, 26) 
AND players.jersey_number > 23


-- Zach Collins and Juancho Hernangomez

SELECT
    players.id, 
    players.first_name, 
    players.last_name, 
    players.birth_date, 
    players.height_inches, 
    players.jersey_number, 
    players.position, 
    players.team_id
FROM players 
JOIN teams ON teams.id = players.team_id 
JOIN divisions ON divisions.id = teams.division_id 
JOIN conferences ON conferences.id = divisions.conference_id
WHERE 
    (teams.code NOT IN ('SAS', 'UTA')) 
AND conferences.name != 'West' 
AND (divisions.abbreviation NOT IN ('SW', 'NW')) 
AND players.position = 'F' 
AND players.height_inches = 81 
AND date_part('YEAR', age(CURRENT_DATE, players.birth_date)) = 26 
AND players.jersey_number > 23 
AND players.jersey_number < 41
