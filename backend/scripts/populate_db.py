"""Simple script to add sensors to the database from a json file

Usage: pyton -m scrips.populate_db rooms.json 

JSON Format:

{
  "rooms": [{"uuid": "jaksdlfja;lskdfj", "number": 123}] 
}

"""


import argparse
import json
import os, sys

from app.database import SessionLocal, engine
from app import models

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    # file_path = os.path.abspath(args['file'])
    file_path = os.path.abspath(args.file_path)
    with open(file_path, "r") as rooms_file:
        json_data = json.load(rooms_file)
        rooms = json_data["rooms"]
        for room in rooms:

            sensor = models.Sensor(uuid=room["uuid"], room_number=room["number"])

            if args.dry_run:
                print(f"Would have saved: {sensor}")
                continue

            print(f"Adding to db: {sensor}")
            db.add(sensor)

    if not args.dry_run:
        should_save = input("Are you sure you want to commit all to the database? y/n")
        if should_save.lower().startswith("y"):
            db.commit()
            print("Commit all to the database")
            sys.exit(0)
        else:
            print("Aborted.")
            sys.exit(1)
