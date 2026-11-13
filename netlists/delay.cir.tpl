* CMOS inverter propagation delay (template)
* Tokens: @VDD@ supply, @SLEW@ input rise/fall time, @CLOAD@ output load, @HALF@ = VDD/2

VDD vdd 0 DC @VDD@
VIN in 0 PULSE(0 @VDD@ 1n @SLEW@ @SLEW@ 9n 20n)
CL out 0 @CLOAD@

* Minimum-size-ish 180 nm inverter (PMOS is 2x wider to balance rise/fall)
MP out in vdd vdd PMOS L=0.18u W=2u
MN out in 0 0 NMOS L=0.18u W=1u

* Generic Level-1 models so no PDK install is needed
.model NMOS NMOS (LEVEL=1 VTO=0.45 KP=120u LAMBDA=0.05)
.model PMOS PMOS (LEVEL=1 VTO=-0.45 KP=60u LAMBDA=0.05)

.tran 10p 40n

* 50% crossings: output falls after input rises (tphl), rises after input falls (tplh)
.meas tran tphl TRIG v(in) VAL=@HALF@ RISE=1 TARG v(out) VAL=@HALF@ FALL=1
.meas tran tplh TRIG v(in) VAL=@HALF@ FALL=1 TARG v(out) VAL=@HALF@ RISE=1

.control
run
quit
.endc
.end
