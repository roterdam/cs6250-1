sudo ovs-vsctl -- --id=@sflow create sflow agent=eth0 target=\"127.0.0.1:6343\" sampling=2 polling=20 -- -- set bridge s1 sflow=@sflow
