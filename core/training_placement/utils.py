import pyotp
from datetime import datetime, timedelta


def send_otp(request):
    time_otp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = time_otp.now()
    request.session['otp_secret_key'] = time_otp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    print('one time password', otp)
