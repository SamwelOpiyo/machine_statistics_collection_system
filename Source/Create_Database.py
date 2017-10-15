import sqlite3

#  connect to a sqlite database(file)
conn = sqlite3.connect('NetworkData.db')
print "Opened database successfully"

#  Create table SystemDetails
conn.execute(("""CREATE TABLE "systemdetails" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "ip_address" char(39) NOT NULL,
              "platform" varchar(30) NOT NULL,
              "date_entry" datetime NULL
);"""))

#  Create table Swap
conn.execute(("""CREATE TABLE "swap" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "total" bigint NULL,
              "used" bigint NULL,
              "free" bigint NULL,
              "percent" decimal NULL,
              "sin" bigint NULL,
              "sout" bigint NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute("""CREATE INDEX "swap_41ba5632" ON "swap" ("ip_id");""")

#  Create table Users
conn.execute(("""CREATE TABLE "systemusers" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "name" varchar(30) NULL,
              "terminal" varchar(30) NULL,
              "host" varchar(30) NULL,
              "started" decimal NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute(("""CREATE INDEX
              "systemusers_41ba5632" ON "systemusers" ("ip_id")
;"""))

#  Create table Network
conn.execute(("""CREATE TABLE "network" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "bytes_sent" bigint NULL,
              "bytes_recv" bigint NULL,
              "packets_sent" bigint NULL,
              "packets_recv" bigint NULL,
              "errin" bigint NULL,
              "errout" bigint NULL,
              "dropin" bigint NULL,
              "dropout" bigint NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute("""CREATE INDEX "network_41ba5632" ON "network" ("ip_id");""")

#  Create table Memory
conn.execute(("""CREATE TABLE "memory" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "total" bigint NOT NULL,
              "available" bigint NOT NULL,
              "percent" decimal NOT NULL,
              "used" bigint NOT NULL,
              "free" bigint NOT NULL,
              "active" bigint NULL,
              "inactive" bigint NULL,
              "buffers" bigint NULL,
              "cached" bigint NULL,
              "shared" bigint NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute("""CREATE INDEX "memory_41ba5632" ON "memory" ("ip_id");""")

#  Create table DiskUsage
conn.execute(("""CREATE TABLE "diskusage" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "total" bigint NOT NULL,
              "used" bigint NOT NULL,
              "free" bigint NOT NULL,
              "percent" decimal NOT NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute("""CREATE INDEX "diskusage_41ba5632" ON "diskusage" ("ip_id");""")

#  Create table DiskPartitions
conn.execute(("""CREATE TABLE "diskpartitions" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "device" varchar(30) NULL,
              "mountpoint" varchar(30) NULL,
              "fstype" varchar(30) NULL,
              "opts" text NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute(("""CREATE INDEX
              "diskpartitions_41ba5632" ON "diskpartitions" ("ip_id")
;"""))

#  Create table CPU
conn.execute(("""CREATE TABLE "cpu" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "cpu_usage" decimal NOT NULL,
              "cpu_count" integer NOT NULL,
              "boot_time" bigint NULL,
              "current_frequency" decimal NULL,
              "min_frequency" decimal NULL,
              "max_frequency" decimal NULL,
              "ctx_switches" bigint NULL,
              "interrupts" bigint NULL,
              "soft_interrupts" bigint NULL,
              "syscalls" bigint NULL,
              "logs" text NULL,
              "date_entry" datetime NULL,
              "ip_id" integer NOT NULL
              REFERENCES "systemdetails" ("id")
);"""))

conn.execute("""CREATE INDEX "cpu_41ba5632" ON "cpu" ("ip_id");""")

print "Table created successfully"

#  close the connection to the database after creating the table
conn.close()
