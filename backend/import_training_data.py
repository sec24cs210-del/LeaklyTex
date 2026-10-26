import pandas as pd

from database import SessionLocal
from models import TrainingData


CSV_FILE = "/Users/kiruba/Downloads/maintenance_prediction_dataset.csv"


def import_training_data():
    df = pd.read_csv(CSV_FILE).iloc[5:]

    db = SessionLocal()

    try:
        records = []

        for _, row in df.iterrows():
            record = TrainingData(
                pressure=row["pressure"],
                flow_rate=row["flow_rate"],
                temperature=row["temperature"],
                vibration=row["vibration"],
                rpm=row["rpm"],
                operational_hours=row["operational_hours"],
                pipe_code=row["pipe_code"],
                zone=row["zone"],
                block=row["block"],
                location_code=row["location_code"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                leakage_flag=bool(row["leakage_flag"]),
            )

            records.append(record)

        db.add_all(records)
        db.commit()

        print(f"Successfully imported {len(records)} training records.")

    except Exception as error:
        db.rollback()
        print("Import failed.")
        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    import_training_data()