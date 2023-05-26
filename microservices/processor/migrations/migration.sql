CREATE TABLE IF NOT EXISTS machines(
    machine_id INT NOT NULL,
    PRIMARY KEY(machine_id)
);

CREATE TABLE IF NOT EXISTS units(
    unit_id INT NOT NULL,
    machine_id INT NOT NULL,
    is_defective BOOLEAN,
    created_at  TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY(unit_id),
    CONSTRAINT fk_machine
        FOREIGN KEY(machine_id)
            REFERENCES machines(machine_id)
);

CREATE TABLE IF NOT EXISTS measurements(
    measurement_id INT GENERATED ALWAYS AS IDENTITY,
    machine_id INT NOT NULL,
    pressure FLOAT,
    temperature FLOAT,
    created_at  TIMESTAMP DEFAULT current_timestamp,
    CONSTRAINT fk_machine
        FOREIGN KEY(machine_id)
            REFERENCES machines(machine_id)
);
