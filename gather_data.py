import pandas as pd
import sqlalchemy
import pymysql


# Read in data from database engine, stored in engine
connection_string = sqlalchemy.URL.create(
    "mysql+pymysql",
    host="mariadb-compx0.oit.utk.edu",
    port=3306,
    database="aspannba_bas476",
    username="hsalitri",
    password="SQL100",
)
print(connection_string)

engine = sqlalchemy.create_engine(connection_string)

pd.read_sql("SHOW TABLES", engine)

Rush2022 = pd.read_sql("SELECT * FROM nfl_rushing_2022 WHERE Pos='RB' ", engine)
Recieve2022 = pd.read_sql("SELECT * FROM nfl_receiving_2022 WHERE Pos='RB' ", engine)
# Pass2022 = pd.read_sql("SELECT * FROM nfl_passing_2022 WHERE Pos='QB'", engine)
# Def2022 = pd.read_sql("SELECT * FROM nfl_defense_2022 ", engine)
# kick2022 = pd.read_sql("SELECT * FROM nfl_kicking_2022 ", engine)
# Punt2022 = pd.read_sql("SELECT * FROM nfl_punting_2022 ", engine)
# Return2022 = pd.read_sql("SELECT * FROM nfl_returns_2022 ", engine)
# Scoring2022 = pd.read_sql("SELECT * FROM nfl_scoring_2022 WHERE Pos='WR' ", engine)
# Scrim2022 = pd.read_sql("SELECT * FROM nfl_scrimmage_2022 ", engine)
# Recieve2023 = pd.read_sql("SELECT * FROM nfl_receiving_2023 ", engine)
# Rush2023 = pd.read_sql("SELECT * FROM nfl_rushing_2023 ", engine)
# Pass2023 = pd.read_sql("SELECT * FROM nfl_passing_2023 WHERE Pos='QB' ", engine)

engine.dispose()

Recieve2022.columns
Rush2022.columns

Rush2022 = Rush2022.drop(["Rk", "1D", "Succ%"], axis=1)
Recieve2022 = Recieve2022.drop(
    ["Rk", "Tm", "Age", "Pos", "G", "GS", "1D", "Succ%", "Player-additional"], axis=1
)


Rush2022.shape
Recieve2022.shape

Run2022 = pd.merge(Rush2022, Recieve2022, how="left", on="Player")
Run2022.shape
Run2022.columns
Run2022.head()

Run2022.to_csv("full_data.csv", index=False)


# --------------------------------------------------------------------------------------#

Run = pd.read_csv("full_data.csv")


# Data cleaning, finding what I want to measure

Run = Run[
    ["Player", "Tm", "Age", "G", "Att", "Yds_x", "TD_x", "Y/A", "Yds_y", "TD_y", "R/G"]
]
# Minimum number of attempts a game for signicant RBs:
Run = Run[(Run["Att"] / Run["G"]) > 6.25]  # At least 6.25 attempts a game
Run = Run[Run["G"] >= 8]  # Played at least 50% of games, I rounded down

# Rename columns for clear understanding to users:
Run = Run.rename(
    columns={
        "Yds_x": "Rush_Yds",
        "TD_x": "Rush_TD",
        "G": "Games",
        "Y/A": "Yds/Rush",
        "Yds_y": "Rec_Yds",
        "TD_y": "Rec_TD",
        "R/G": "Receptions/G",
    }
)


Run["Total_TDs"] = Run["Rush_TD"] + Run["Rec_TD"]
Run["Total_Yds"] = Run["Rush_Yds"] + Run["Rec_Yds"]

Run = Run.drop(["Att", "Rush_TD", "Rec_TD", "Games"], axis=1)

Run


# -----------------------------------------------------------------------#


# Total yardage (Totalyds)
Totalyds = Run.sort_values("Total_Yds", ascending=False)

# Column to move closer to the front, rearranging some columns
ctm = Totalyds.pop("Total_Yds")
ctm2 = Totalyds.pop("Age")
ctm3 = Totalyds.pop("Rec_Yds")
Totalyds.insert(2, "Total_Yds", ctm)
Totalyds.insert(7, "Age", ctm2)
Totalyds.insert(4, "Rec_Yds", ctm3)

# Strip anything that isnt a letter in player name, easier for user to manipulate
Totalyds["Player"] = Totalyds["Player"].str.replace("*", "")
Totalyds["Player"] = Totalyds["Player"].str.replace("+", "")

Totalyds.head()


# Convert to summarized_view for analysis
Totalyds.to_csv("summarized_view.csv", index=False)


# ----------------------------------------------------------------------#
