import snowflake.connector as sf

ctx = sf.connect(
user="CONNECTWITHSABYA2022",
password = "QAWS123qaws@",
account = "igvvxms-PYB14977",
warehouse="COMPUTE_WH",
database ="ecommerce_db",
schema="ECOMMERCE_DEV",
role="sysadmin",
session_parameters={
    'TIMEZONE' : 'UTC',
}
)

cs = ctx.cursor();

try:

        sql = """select * from LINEITEM limit 10"""
        cs.execute(sql)
        all_rows=cs.fetchall()
        print(all_rows)
finally:
        cs.close()
ctx.close()