import hashlib

m = hashlib.sha1()
m.update(
    b"""To the Director of the Scientific and Technical Library
Of Igor Sikorsky KPI
Petrenko PP
student from group KM-81 FAM
Verzun Polina

statement.
Please extend the storage period of the book issued to me on 30.12.2020
"Hypergraphs theory and practice" until 30.01.2021 inclusive.

16/12/2020

Verzun Polina"""
)
m.digest()
print(m.hexdigest())
