Python script to check backend health of varnish

How to run script:

```
usage: check_varnish_health [-h] path args

./check_backend_health.py [varnishadm path] [backend cmd (backend.list)]
```

Example Nagios Configuration:
```
command[check_backend_health]=/usr/lib/nagios/plugins/check_backend_health.py /usr/bin/varnishadm backend.list
```

Example Output:
```
~# /usr/lib/nagios/plugins/check_nrpe -u -H [IP Address/Hostname] -c check_backend_health
OK: All 4 backends are healthy   
```
