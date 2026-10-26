from datetime import datetime, date

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Pipe(Base):
    """
    Stores information about each physical pipe/pipe segment.
    This is the main asset table for LeaklyTex.
    """

    __tablename__ = "pipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    pipe_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    material: Mapped[str] = mapped_column(String(50), nullable=False)

    installation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    diameter_mm: Mapped[float | None] = mapped_column(Float, nullable=True)

    length_m: Mapped[float | None] = mapped_column(Float, nullable=True)

    location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 0.0 = very low corrosion, 1.0 = severe corrosion
    corrosion_level: Mapped[float | None] = mapped_column(Float, nullable=True)

    previous_failures: Mapped[int] = mapped_column(Integer, default=0)

    status: Mapped[str] = mapped_column(
        String(30),
        default="active"
    )

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    sensor_readings = relationship(
        "SensorReading",
        back_populates="pipe"
    )

    maintenance_records = relationship(
        "MaintenanceRecord",
        back_populates="pipe"
    )

    predictions = relationship(
        "Prediction",
        back_populates="pipe"
    )


class SensorReading(Base):
    """
    Stores sensor readings received from the ESP32 system.
    """

    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    pipe_id: Mapped[int] = mapped_column(
        ForeignKey("pipes.id"),
        nullable=False,
        index=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)

    flow_rate: Mapped[float | None] = mapped_column(Float, nullable=True)

    vibration: Mapped[float | None] = mapped_column(Float, nullable=True)

    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)

    h2s_level: Mapped[float | None] = mapped_column(Float, nullable=True)
    rpm: Mapped[float | None] = mapped_column(Float, nullable=True)

    operational_hours: Mapped[float | None] = mapped_column(Float, nullable=True)

    pipe = relationship(
        "Pipe",
        back_populates="sensor_readings"
    )


class MaintenanceRecord(Base):
    """
    Stores inspection, repair and replacement history.
    """

    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    pipe_id: Mapped[int] = mapped_column(
        ForeignKey("pipes.id"),
        nullable=False
    )

    maintenance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    maintenance_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    cost: Mapped[float | None] = mapped_column(
        Numeric,
        nullable=True
    )

    technician: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    pipe = relationship(
        "Pipe",
        back_populates="maintenance_records"
    )


class Prediction(Base):
    """
    Stores risk and leak predictions.

    Initially this can store the rule-based placeholder.
    Later it can store predictions from the ML model.
    """

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    pipe_id: Mapped[int] = mapped_column(
        ForeignKey("pipes.id"),
        nullable=False
    )

    prediction_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Risk value between 0.0 and 1.0
    risk_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    risk_level: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    leak_detected: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    # ML model confidence, when available
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    model_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    recommended_action: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    pipe = relationship(
        "Pipe",
        back_populates="predictions"
    )
class TrainingData(Base):
    """
    Stores historical dataset records used for ML model training.
    """

    __tablename__ = "training_data"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)

    flow_rate: Mapped[float | None] = mapped_column(Float, nullable=True)

    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)

    vibration: Mapped[float | None] = mapped_column(Float, nullable=True)

    rpm: Mapped[float | None] = mapped_column(Float, nullable=True)

    operational_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    pipe_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    zone: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    block: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    location_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    leakage_flag: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )