DROP TABLE IF EXISTS t_maintenance_info;

CREATE TABLE t_maintenance_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  system_name TEXT NOT NULL,
  start_dt TIMESTAMP NOT NULL,
  end_dt TIMESTAMP NOT NULL,
  created_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
