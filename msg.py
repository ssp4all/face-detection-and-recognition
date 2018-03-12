import way2sms

q = way2sms.sms(9892420886, 'motionsensor')
q.send('9892420886', 'Intruder Alert')
q.logout()
