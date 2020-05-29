import logging.config
# log level constant definitions
DESTINATION_EMAIL = 'nkrause@ucsd.edu'
LOG_DEBUG = 'debug'
LOG_INFO = 'info'
LOG_WARNING = 'warning'
LOG_ERROR = 'error'
LOG_CRITICAL = 'critical'
level_scale = {LOG_DEBUG : logging.DEBUG , LOG_INFO : logging.INFO, LOG_WARNING : logging.WARNING,\
    LOG_ERROR : logging.ERROR, }
from socket import gethostname
hostname = gethostname()

# independent function
def notify_email(notification_str, subject='ASAP Log Notification', level=LOG_INFO):
    """send a notification to nkrause@ucsd.edu, Level should be a str that corresponds
     to the notification urgency(info, warning, critical)"""
    import smtplib
    from email.mime.text import MIMEText
    
    message = MIMEText(notification_str)
    port = 25
    message['To']= DESTINATION_EMAIL
    message['From']= 'ASAP Log {host} <asap-log@ucsd.edu>'.format(host=hostname.split('.')[0].upper())
    message['Subject']= '[{level}] {subject}'.format(level=level, subject=subject)

    server = smtplib.SMTP("smtp.ucsd.edu", port)
    server.set_debuglevel(False)  # show communication with the server
    try:
        server.sendmail(message['From'], message['To'], message.as_string())
    except Exception as e:
        log('Failed to send mail: ' + str(e), level=LOG_ERROR, email=False)  # this could cause a loop if all errors are  set to be emailed
        return False
    server.quit()
    log('Sent mail to {destination} from {source}'.format(destination=message['To'], source=message['From']))
    
    return True

def log(message, level='info', email=False, subject=None, err_str=None):
    """Consolidate logging into one function call. Easier to redirect from one location"""
    if err_str is not None:
        message += '\n\n\tERROR:\n\t' + err_str 
    getattr(LogASAP.logger, level)(message)    # calls appropriate log function (depends on level)
    logging.getLogger('LOGASAP')
    if email or level is LOG_CRITICAL:  # explicitly called to email or it's a critical log
        if subject is None:
            notify_email(message, level=level)
        else:
            notify_email(message, level=level, subject=subject)

def setup_log(level=logging.DEBUG, destination=None):
    """Defines the logging level and where logs should be written to"""
    # TODO implement destination--> file, or some persistent log
    # logging.basicConfig(level=level,
    #                 format='%(asctime)s %(name)s [%(levelname)s] %(message)s')
                    # filename='/tmp/myapp.log',
                    # filemode='w')
    logging.config.fileConfig('/home/nate/ASAP/Log/logging.conf')   
    LogASAP.logger = logging.getLogger('LOGASAP')  # reassign program logger


class LogASAP:
    logger = logging.getLogger() # gets the default root logger until this is changed
