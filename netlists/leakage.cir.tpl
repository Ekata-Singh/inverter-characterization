* CMOS inverter static leakage (template)
* Tokens: @VDD@ supply, @VIN@ held input level (0 or @VDD@)

VDD vdd 0 DC @VDD@
VIN in 0 DC @VIN@
CL out 0 1f

MP out in vdd vdd PMOS L=0.18u W=2u
MN out in 0 0 NMOS L=0.18u W=1u

.model NMOS NMOS (LEVEL=1 VTO=0.45 KP=120u LAMBDA=0.05)
.model PMOS PMOS (LEVEL=1 VTO=-0.45 KP=60u LAMBDA=0.05)

.tran 10p 10n

* Average supply current once the output has settled (5 ns to 10 ns)
.meas tran ileak AVG I(VDD) FROM=5n TO=10n

.control
run
quit
.endc
.end
