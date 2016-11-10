#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Copyright (c) 2016 François Wautier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
#
import sqlalchemy as sa
import datetime as dt

data= { "Latkrabang": {"latitude":13.730156,"longitude":100.779966, "contact":"john.cl@silly-walk.com"},
        "Khon Khaen": {"latitude":16.439039,"longitude":102.827537, "contact":"eric.id@nudge-nudge.net"},
        "Chiang Mai": {"latitude":18.762921,"longitude":98.994452,  "contact":"michael.pa@spanish-inquisition.org"},
        "Phuket":     {"latitude":7.988232, "longitude":98.425437,  "contact":"graham.ch@brian.info"},
        "Pattaya":    {"latitude":12.925610,"longitude":100.871945, "contact":"terry.jo@nudepianist.xxx"},
        "Samui":      {"latitude":9.444260, "longitude":100.022984, "contact":"terry.gi@gumby.gov"},
        "Phan Ngan":  {"latitude":9.771981, "longitude":99.966143,  "contact":"carol.cl@comeupstair.co.uk"}}
        
eng=sa.create_engine("sqlite:///:memory:")
metadata=sa.MetaData()
station = sa.Table('station', metadata,
     sa.Column('id', sa.Integer, primary_key=True),
     sa.Column('name', sa.String(32), unique=True),
     sa.Column('contact', sa.String(64), nullable=False),
     sa.Column('latitude', sa.Float, nullable=False),
     sa.Column('longitude', sa.Float, nullable=False),
)

measurement=sa.Table('measurement', metadata,
     sa.Column('id', sa.Integer, primary_key=True),
     sa.Column('station_id', None, sa.ForeignKey('station.id')),
     sa.Column('value', sa.Float),
     sa.Column('units',sa.String(8)),
     sa.Column("date",sa.DateTime)
)

metadata.create_all(eng)


eng.execute(station.insert(),[ {**data[x],**{"name":x}} for x in data])      

print ("==========\nAll stations' record\n==========")
resu=eng.execute(station.select())
for a in resu:
    print(a)

print ("==========\nAll names\n==========")
resu=eng.execute(station.select())
for a in resu:
    print(a.name)
    
print ("==========\nNobody expects the Spanish Inquisition\n==========")
resu=eng.execute(station.select().where (station.c.latitude > 18))
for a in resu:
     print(a)


eng.execute(measurement.insert(),[ {"station_id":3,"value": 32, "units":"mm","date":dt.datetime.strptime("1969-10-05 22:15:00","%Y-%m-%d %H:%M:%S")} ])
print ("==========\nCartesian Product\n==========")
resu=eng.execute(sa.select([station,measurement]))
for a in resu:
     print(a)
    
print ("==========\nJoin\n==========")
resu=eng.execute(sa.select([station,measurement]).where (station.c.id == measurement.c.station_id))
for a in resu:
     print(a)