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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
import sqlalchemy as sa
import datetime as dt

data= { "Latkrabang": {"latitude":13.730156,"longitude":100.779966, "contact":"john.cl@silly-walk.gov"},
        "Khon Khaen": {"latitude":16.439039,"longitude":102.827537, "contact":"eric.id@nudge-nudge.net"},
        "Chiang Mai": {"latitude":18.762921,"longitude":98.994452,  "contact":"michael.pa@spanish-inquisition.org"},
        "Phuket":     {"latitude":7.988232, "longitude":98.425437,  "contact":"graham.ch@brian.info"},
        "Pattaya":    {"latitude":12.925610,"longitude":100.871945, "contact":"terry.jo@nudepianist.xxx"},
        "Samui":      {"latitude":9.444260, "longitude":100.022984, "contact":"terry.gi@gumby.gov"},
        "Phan Ngan":  {"latitude":9.771981, "longitude":99.966143,  "contact":"carol.cl@comeupstair.co.uk"}}
        
eng=sa.create_engine("sqlite:///:memory:")
Base=declarative_base()

class Station(Base):
    __tablename__='station'
    id = sa.Column(sa.Integer, sa.Sequence("station_id_seq"), primary_key=True)
    name = sa.Column( sa.String(32), unique=True )
    contact = sa.Column( sa.String(64), nullable=False )
    latitude = sa.Column( sa.Float, nullable=False )
    longitude = sa.Column( sa.Float, nullable=False )
    
    measurements = relationship("Measurement", order_by="Measurement.date", backref="station")
    
    def __repr__(self):
        if self.latitude>=0:
            latstr="%.3f° north, "%self.latitude
        else:
            latstr="%.3f° south,"%(0.0-self.latitude)
        if self.longitude>=0:
            lonstr="%.3f° east "%self.longitude
        else:
            lonstr="%.3f° west "%(0.0-self.longitude)
        resu=self.name+" at "+latstr+lonstr+"managed by "+self.contact
        for x in self.measurements:
            resu+="\n\t"+str(x)
        return resu

class Measurement(Base):
    __tablename__='measurement'
    id = sa.Column( sa.Integer, sa.Sequence("meas_id_seq"), primary_key=True )
    station_id = sa.Column( None, sa.ForeignKey('station.id') )
    value = sa.Column( sa.Float )
    units = sa.Column( sa.String(8) )
    date = sa.Column( sa.DateTime )
    
    def __repr__(self):
        return "%.2f %s on %s" % (self.value, self.units, self.date.strftime("%B %d, %Y at %H:%m"))


Base.metadata.create_all(eng)

Session = sessionmaker(bind=eng)
sess=Session()

for st in [ {**data[x],**{"name":x}} for x in data ]:
    ast=Station(**st)
    sess.add(ast)

sess.commit()
print ("==========\nAll stations\n==========")
for x in sess.query(Station).all():
    print(x)
    
print ("==========\nPhuket stations\n==========")
ast=sess.query(Station).filter_by(name="Phuket").one()
print(ast)

print ("==========\nNobody expects the Spanish Inquisition\n==========")
ast=sess.query(Station).filter(Station.latitude>18).one()
print(ast)

meas=Measurement(value=32,units="mm",date=dt.datetime.strptime("1969-10-05 22:15:00","%Y-%m-%d %H:%M:%S"))
ast.measurements.append(meas)
meas=Measurement(value=12,units="mm",date=dt.datetime.strptime("1970-01-11 22:15:00","%Y-%m-%d %H:%M:%S"))
ast.measurements.append(meas)

sess.commit()
print ("==========\nStill nobody expects the Spanish Inquisition\n==========")
ast=sess.query(Station).filter(Station.latitude>18).one()
print(ast)


