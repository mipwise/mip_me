from mip_me import input_schema
path = "test_mip_me/data/inputs"
dat = input_schema.csv.create_pan_dat(path)
print(dat)

