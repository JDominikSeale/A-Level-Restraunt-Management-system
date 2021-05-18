import smtplib

#85952248386-1bsiasspv2k5pn33s7e2r6si66jagf38.apps.googleusercontent.com - Client ID
#S6a0ixKhk_veGk3ustTMHiXZ - client secret


def emailSend(customerEmail, order, customerPaid, ID):
    myEmail = 'georgndragon@gmail.com'
    password = 'BurnleyPassword7'
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(myEmail, password)
    m = 'Thank you for coming to the George and Dragon, please find your receipt below:\n'
    for i in order:
        m += "%s \n" % str(i[0])
    m += "£%s \n" % str(customerPaid)
    m += "Receipt ID: %s" % str(ID)
    print(m)
    s.sendmail(myEmail, str(customerEmail), str(m))
    s.quit()