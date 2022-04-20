import smtplib
from email.message import EmailMessage


# class GMailClient:
def sendEmail(contacts):
    #EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    #EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    EMAIL_ADDRESS = 'mrakesh22@jnn.edu.in'
    EMAIL_PASSWORD = '9543157971'

    #contacts = ['dineshraturi22@gmail.com']

    msg = EmailMessage()
    msg['Subject'] = 'Detailed Covid-19 Report!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts[2]

    values = contacts[3]
    msg.set_content("Hello Mr. {} Here is your Covid 19 Report PFA".format("rakesh"))
    #print(contacts[2])
    # email_message = template.read_course_template("simple")
    email_message = open(r"BestCovid19_bot-DialogFlow-master\DLM_Template.html", "r")
    email_message = email_message.read()
    #print(email_message)
    country_name1 = contacts[4]
    total1 = str(values.get("total"))
    new1 = str(values.get("new"))
    active1 = str(values.get("active"))
    critical1 = str(values.get("critical"))
    recovered1 = str(values.get("recovered"))
    # print(new1 + total1)
    #.format(code1=code1, code2=code2, code3=code3, code4=code4, code5=code5

    '''msg.add_alternative(email_message.format(country_name=country_name1, total=total1, new=new1, active=active1, critical=critical1,
                                    recovered=recovered1,subtype='html'))'''



    msg.add_alternative(email_message.format(country_name=country_name1, total=total1, new=new1, active=active1, critical=critical1,
                                recovered=recovered1), subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# sendEmail([1,2,3,4,5])