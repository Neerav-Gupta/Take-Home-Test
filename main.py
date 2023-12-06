import tbaapiv3client
from tbaapiv3client.rest import ApiException

userTeam = str(input("Please Enter the Team Number: "))
userYear = int(input("Please Enter the Year you Want to Check for: "))
team_key = "frc" + userTeam

configuration = tbaapiv3client.Configuration(
    host="https://www.thebluealliance.com/api/v3",
    api_key={
        "X-TBA-Auth-Key": "RHcSmpJC8aeNBOvlZMQ6yAqAmpeC6IDLOAFLBrM9x2h92J0mMI1wtUjBhfSI3mPV"
    },
)

with tbaapiv3client.ApiClient(configuration) as api_client:
    api_instance = tbaapiv3client.TeamApi(api_client)

    try:
        allEvents = api_instance.get_team_events(team_key)
        print()
        print("Events Participated in {a} by Team {b}".format(a=userYear, b=userTeam))
        print(
            "------------------------------------"
            + ("-" * (len(userTeam) + len(str(userYear))))
        )
        events = []
        for i in range(len(allEvents)):
            event = allEvents[i]
            if event.year == userYear:
                print(event.name, "at", event.location_name, "on", event.start_date)
                events.append([event.name, event.key])

        print()
        print("Teams Which Participated In Each Event")
        print("--------------------------------------")
        teams = []
        for i in range(len(events)):
            allTeams = api_instance.get_event_teams(events[i][1])
            print(events[i][0] + ":")
            for team in allTeams:
                print(team.nickname, ":", team.team_number, end=", ")
                teams.append(
                    [
                        team.nickname,
                        team.team_number,
                        team.country,
                        team.state_prov,
                        team.city,
                    ]
                )
            print()
            print()

        print()
        print("Unique Teams and Other Info")
        print("---------------------------")
        team_name = list(set(i[0] for i in teams))
        team_number = list(set(i[1] for i in teams))
        for name, number in zip(team_name, team_number):
            print(name, ":", number, end=", ")
        print()
        print()

        countries = list(set(i[2] for i in teams))
        for country in countries:
            print(country, end=", ")
        print()
        print()

        states = list(set(i[3] for i in teams))
        for state in states:
            print(state, end=", ")
        print()
        print()

        cities = list(set(i[4] for i in teams))
        for city in cities:
            print(city, end=", ")
        print()
        print()

    except ApiException as e:
        print("Exception: %s\n" % e)
