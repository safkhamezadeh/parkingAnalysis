-- 001_initial_schema.sql
-- project -> parking_lot -> parking_spot -> observation (per frame and spot)
-- Images are not stored (frame keeps only a filename); polygons live in JSON files on disk, not in the DB.
--
-- Note: foreign keys are only enforced if each connection runs `PRAGMA foreign_keys = ON;`
-- (do this in db.py when opening the database).

-- A client, or one of your own datasets ('PKLot dataset', 'Own tests').
CREATE TABLE project (
    project_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    notes       TEXT
);

CREATE TABLE parking_lot (
    lot_id      INTEGER PRIMARY KEY,
    project_id  INTEGER NOT NULL REFERENCES project(project_id),
    name        TEXT NOT NULL,
    notes       TEXT
);

-- The physical spot: facts about the lot that do not change when the camera moves.
CREATE TABLE parking_spot (
    spot_id     INTEGER PRIMARY KEY,
    lot_id      INTEGER NOT NULL REFERENCES parking_lot(lot_id),
    zone        TEXT,                               -- free text for reporting groups (e.g. 'P1 staff'); nullable, fill in after calibration
    label       TEXT NOT NULL,                      -- e.g. 'A12'
    spot_type   TEXT NOT NULL DEFAULT 'regular'
                CHECK (spot_type IN ('regular', 'disabled', 'ev', 'motorcycle', 'reserved', 'loading')),
    UNIQUE (lot_id, label)
);

-- One camera position + calibration. Moving or recalibrating the camera => new session.
CREATE TABLE session (
    session_id  INTEGER PRIMARY KEY,
    lot_id      INTEGER NOT NULL REFERENCES parking_lot(lot_id),
    source      TEXT NOT NULL
                CHECK (source IN ('pklot', 'own_video', 'pilot')),
    folder      TEXT NOT NULL,                      -- this session's folder (frames, polygon JSON), relative to the data root
    status      TEXT NOT NULL DEFAULT 'not_started'
                CHECK (status IN ('not_started', 'ongoing', 'finished')),
    started_at  TIMESTAMP
                CHECK (started_at IS NULL OR datetime(started_at) IS NOT NULL),   -- ISO 8601
    end_date    DATE
                CHECK (end_date IS NULL OR date(end_date) IS NOT NULL),           -- YYYY-MM-DD; set when finished
    notes       TEXT
);

CREATE TABLE frame (
    frame_id    INTEGER PRIMARY KEY,
    session_id  INTEGER NOT NULL REFERENCES session(session_id),
    ts          TIMESTAMP NOT NULL
                CHECK (datetime(ts) IS NOT NULL),   -- capture time, ISO 8601 (e.g. 2025-07-14T09:30:00)
    filename    TEXT NOT NULL,
    UNIQUE (session_id, filename)
);

-- Long format: one row per frame and spot. Curves, heatmaps and dwell runs are queries on this.
CREATE TABLE observation (
    frame_id    INTEGER NOT NULL REFERENCES frame(frame_id),
    spot_id     INTEGER NOT NULL REFERENCES parking_spot(spot_id),
    occupied    INTEGER NOT NULL CHECK (occupied IN (0, 1)),
    confidence  REAL,                               -- best matching detection score
    PRIMARY KEY (frame_id, spot_id)
);

CREATE INDEX idx_frame_ts ON frame(session_id, ts);
CREATE INDEX idx_spot_lot ON parking_spot(lot_id, zone);
CREATE INDEX idx_observation_spot ON observation(spot_id);