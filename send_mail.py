import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def Usage():
    print('send_mail.py usage:')    
    print('-h, --help    : print help message')
    print('-mf           : read message from a file, input absolute path and file name')
    print('-m, --message : input message in email body')
    print('-s, --subject : input specific subject')
    print('''-t, --to      : input email receiver, need only id before @
       example: jay-18019;abc-00001;edf-00002''')

def message(mm):
    msg.attach(MIMEText(str(mm)))

def message_file(path_file):
    with open(path_file) as fp:
        abc = MIMEText(fp.read())
    msg.attach(abc)
	
def main(argv):
    global msg
    msg = MIMEMultipart('alternative')
    email_smtp='email.esunbank.com.tw'
    you=''

    msg['Subject'] = '[Auto-Message]'
    msg['From'] = 'quant-team'

    if len(argv)==1:
        Usage()
        sys.exit(2)

    for i in range(1,len(argv)):
        if argv[i] == '-h' or argv[i] == '--help':
            Usage()
            sys.exit(1)
        elif argv[i] == '-mf':
            message_file(argv[i+1])
        elif argv[i] == '-m' or argv[i] == '--message' and argv[i] != '-mf':
            message(argv[i+1])
        elif argv[i] == '-s' or argv[i] == '--subject':
            msg['Subject'] = str(argv[i+1])
        elif argv[i] == '-t' or argv[i] == '--to':
            lists=[]
            lists=str(argv[i+1]).split(';')
            for mto in lists:
                if mto!='':
                    you=you + mto + '@' + email_smtp + ';'
					
    if you=='':
	    you='jay-18019@' + email_smtp

    msg['To'] = you	
    s = smtplib.SMTP(email_smtp)
    s.send_message(msg)
    s.quit()
    print('Sending email successfully!!')			
			
if __name__ == '__main__':
    main(sys.argv)