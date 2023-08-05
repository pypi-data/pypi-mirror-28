from __future__ import print_function
import sys, os
import re, argparse, collections, datetime, dateutil, boto3, psutil, logging, json, atexit
from six.moves import configparser as ConfigParser
from builtins import input
from yapsy import PluginManager

__version__ = '2.1.3'

#initialize logging
logging.getLogger('yapsy').addHandler(logging.StreamHandler())
log = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
logHandler.setFormatter(logging.Formatter('%(name)s.%(funcName)s : %(message)s'))
log.addHandler(logHandler)
def logDatetimeConverter(o): return o.__str__() if isinstance(o, datetime.datetime) else o

#get cross-platform home directory
HOME_PATH = os.path.expanduser('~')
AWS_CONFIG_FILE = HOME_PATH + '/.aws/config'
AWS_CREDENTIALS_FILE = HOME_PATH + '/.aws/credentials'
AWS_CACHE_DIRECTORY = HOME_PATH + '/.aws/cli/cache/'

class OutData():
    """
    Contains the data to be sent to the shell wrappers;
    Will only store the first data added to it
    """
    data = ''
    def set_data(self, added_data):
        log.info("Setting Data!")
        if not self.data:
            log.debug("Data Set: " + str(added_data))
            self.data = added_data
    def print_data(self):
        log.info("Sending data to shell wrappers!")
        log.debug("Data: " + str(self.data))
        print(self.data)

def generate_awsume_argument_parser():
    """
    Generate ArgParse's argument parser for AWSume
    """
    log.info('generate_awsume_argument_parser')

    return argparse.ArgumentParser(description='AWSume')

def parse_arguments(argumentParser, sysArgs):
    """
    commandLineArguments - a list of arguments;
    parse through the arguments
    """
    log.info('Parsing Arguments')

    return argumentParser.parse_args(sysArgs)

def add_arguments(argumentParser):
    """
    argumentParser - the argparse argument parser;
    add all the default arguments to AWSume
    """
    log.info('Adding arguments')

    #profile name argument
    argumentParser.add_argument(action='store', dest='profile_name',
                                nargs='?', metavar='profile name',
                                help='The profile name')
    #default flag
    argumentParser.add_argument('-d', action='store_true', default='False',
                                dest='default',
                                help='Use the default profile')
    #show flag (only used for the shell wrapper)
    argumentParser.add_argument('-s', action='store_true', default=False,
                                dest='show',
                                help='Show the commands to assume the role')
    #refresh flag
    argumentParser.add_argument('-r', action='store_true', default=False,
                                dest='refresh',
                                help='Force refresh the session')
    #auto-refresh flag
    argumentParser.add_argument('-a', action='store_true', default=False,
                                dest='auto_refresh',
                                help='Enable auto-refreshing role credentials')
    #kill auto-refresher flag
    argumentParser.add_argument('-k', action='store_true', default=False,
                                dest='kill',
                                help='Kill the auto-refreshing process')
    #display version flag
    argumentParser.add_argument('-v', action='store_true', default=False,
                                dest='version',
                                help='Display the current version of AWSume')
    #list profile data flag
    argumentParser.add_argument('-l', action='store_true', default=False,
                                dest='list_profiles',
                                help='List useful information about available profiles')
    #set Session name
    argumentParser.add_argument('--session-name',  default=None, dest='sessionname',
                                help='set Session Name')
    #list roles/users
    argumentParser.add_argument('--rolesusers', action='store_true', default=False,
                                dest='rolesusers',
                                help='List all awsume-able roles/users')

    #info flag
    argumentParser.add_argument('--info', action='store_true',
                                dest='info',
                                help='Print any info logs to stderr')
    #debug flag
    argumentParser.add_argument('--debug', action='store_true',
                                dest='debug',
                                help='Print any debug logs to stderr')
    return argumentParser

def print_version():
    log.info('Printing Version')

    print('Version' + ' ' + __version__)

def set_default_flag(arguments):
    log.info('Setting the default flag')

    #make sure we always look at the default profile
    #arguments.profile_name = 'default'
    arguments.default = True

def handle_command_line_arguments(arguments, app, out_data):
    """
    arguments - the arguments to handle;
    scan the arguments for anything special that only requires one function call and then exit
    """
    log.info('Handling command-line arguments')

    #check for debug/info flags
    if arguments.info:
        log.setLevel(logging.INFO)
    if arguments.debug:
        log.setLevel(logging.DEBUG)
    log.info('Info logs are visible')
    log.debug('Debug logs are visible')

    #check for version flag
    if arguments.version:
        print_version()
        exit(0)

    #check for list roles and users flag
    if arguments.rolesusers:
        #get the list of roles and users
        rolesUsers = []
        for func in app.list_roles_users_funcs:
            rolesUsers.extend(func())

        for item in rolesUsers:
            print(item, end='\n')
        exit(0)

    #check for list profiles flag
    if arguments.list_profiles:
        #get the list of config profiles
        configProfileList = collections.OrderedDict()
        for func in app.get_config_profile_list_funcs:
            configProfileList.update(func(arguments, out_data, AWS_CONFIG_FILE))

        #get the list of credentials profiles
        credentialsProfileList = collections.OrderedDict()
        for func in app.get_credentials_profile_list_funcs:
            credentialsProfileList.update(func(arguments, AWS_CREDENTIALS_FILE))

        list_profile_data(configProfileList, credentialsProfileList)
        exit(0)

    #check for the kill auto-refresher flag
    if arguments.kill:
        stop_auto_refresh(out_data, arguments.profile_name, AWS_CREDENTIALS_FILE)
        exit(0)

    if arguments.profile_name is None or arguments.profile_name == 'default':
        set_default_flag(arguments)

def get_profiles_from_ini_file(iniFilePath):
    """
    iniFilePath - the file to create a parser out of;
    return a dict of sections from the file
    """
    log.info('Getting profiles from the INI file')

    if os.path.exists(iniFilePath):
        iniFileParser = ConfigParser.ConfigParser()
        iniFileParser.read(iniFilePath)
        for section in iniFileParser._sections:
          iniFileParser._sections[section]['__name__'] = section
        return iniFileParser._sections
    print('AWSume Error: Trying to access non-existant file path: ' + iniFilePath, file=sys.stderr)
    exit(1)

def get_ini_profile_by_name(iniProfileName, iniProfiles):
    """
    iniProfileName - the name of the profile to return;
    iniProfiles - the dict of ini profiles to search through;
    return the profile under the name given by `iniProfileName`
    """
    log.info('Getting the INI profile by name')

    #check if profile exists
    if iniProfileName in iniProfiles:
        return iniProfiles[iniProfileName]
    #if profile doesn't exist, return an empty OrderedDict
    return collections.OrderedDict()

def get_config_profile_list(arguments, out_data, configFilePath=AWS_CONFIG_FILE):
    """
    arguments - the command-line arguments;
    configFilePath - the path to the config file;
    get the list of config profiles from the config file
    """
    log.info('Getting the config profile list')

    return get_profiles_from_ini_file(configFilePath)

def get_credentials_profile_list(arguments, out_data, credentialsFilePath=AWS_CREDENTIALS_FILE):
    """
    arguments - the command-line arguments;
    credentialsFilePath - the path to the config file;
    get the list of credentials profiles from the credentials file
    """
    log.info('Getting the credentials profile list')

    return get_profiles_from_ini_file(credentialsFilePath)

def get_config_profile(configProfiles, arguments, out_data):
    """
    configProfiles - the list of config profiles;
    arguments - the command-line arguments;
    return the config profile from the given command-line arguments
    """
    log.info('Getting the config profile')

    if arguments.default is True:
        return get_ini_profile_by_name('default', configProfiles)
    else:
        return get_ini_profile_by_name('profile ' + arguments.profile_name, configProfiles)

def get_credentials_profile(credentialsProfiles, configSection, arguments, out_data, credentialsPath=AWS_CREDENTIALS_FILE):
    """
    credentialsProfiles - the list of credentials profiles;
    configSection - the config profile that tells which credentials profile to get;
    arguments - the command-line arguments;
    credentialsPath - the path to the credentials file
    return the appropriate credentials file, whether `configSection` is a role or user profile
    """
    log.info('Getting the credentials profile')

    #get the credentials file, whether that be a source_profile or the other half of a user profile
    if is_role_profile(configSection):
        log.debug('Profile is a role, getting the source profile')
        #grab the source profile
        sourceProfile = get_ini_profile_by_name(configSection['source_profile'], credentialsProfiles)
        return sourceProfile
    else:
        log.debug('Profile is a user, getting the user access keys')
        #the rest of the user, from the credentials file
        if arguments.default is True:
            returnProfile = get_ini_profile_by_name('default', credentialsProfiles)
        else:
            returnProfile = get_ini_profile_by_name(arguments.profile_name, credentialsProfiles)
        return returnProfile

def validate_profiles(configSection, credentialsSection):
    """
    configSection - the config profile from the config file;
    credentialsSection - the credentials profile from the credentials file;
    check that `configSection` and `credentialsSection` are valid, if not exit
    """
    log.info('Validating profiles')

    #if the profile doesn't exist, leave
    if not configSection and not credentialsSection:
        print('AWSume Error: Profile not found', file=sys.stderr)
        exit(1)
    #make sure credentials profile has its credentials
    validate_credentials_profile(credentialsSection)

def handle_profiles(configSection, credentialsSection, arguments, out_data):
    """
    configSection - the config profile from the config file;
    credentialsSection - the credentials profile from the credentials file;
    validate profiles and check for any special cases
    """
    log.info('Handling profiles')

    #validate the profiles
    validate_profiles(configSection, credentialsSection)

    #if the user is AWSuming a user profile, and no mfa is required
    #no more work is required
    if not is_role_profile(configSection) and not requires_mfa(configSection):
        log.debug('Profile is not a role and does not require mfa, exporting credentials')
        user_out_data = 'Awsume' +  ' ' + \
                        str(credentialsSection.get('aws_secret_access_key')) + ' ' + \
                        'None' + ' ' + \
                        str(credentialsSection.get('aws_access_key_id')) + ' ' + \
                        str(configSection.get('region')) + ' '
        if arguments.profile_name != None:
            user_out_data += str(arguments.profile_name)
        else:
            user_out_data += 'Default'
        out_data.set_data(user_out_data)

def requires_mfa(profileToCheck):
    """
    profileToCheck - a config profile;
    return whether or not `profileToCheck` requires mfa
    """
    log.info('Checking if the profile requires MFA')

    if 'mfa_serial' in profileToCheck:
        log.debug('The profile requires MFA')
        return True
    log.debug('The profile does not require MFA')
    return False

def get_user_credentials(configSection, credentialsSection, userSession, cachePath, arguments, out_data):
    """
    configSection - the profile from the config file;
    credentialsSection - the profile from the credentials file;
    arguments - the command-line arguments passed into AWSume;
    get credentials for the user
    """
    log.info('Getting User Credentials')

    cacheFileName = 'awsume-temp-' + credentialsSection['__name__']
    cacheSession = read_awsume_session_from_file(cachePath, cacheFileName)
    #verify the expiration, or if the user wants to force-refresh
    if arguments.refresh or not is_valid_awsume_session(cacheSession):
        log.debug('Getting new credentials')
        #the boto3 client used to make aws calls
        log.debug('Creating the user client')
        userClient = create_boto_sts_client(credentialsSection['__name__'])
        #set the session
        awsUserSession = get_session_token_credentials(userClient, configSection)
        userSession = create_awsume_session(awsUserSession, configSection)
        #cache the session
        write_awsume_session_to_file(cachePath, cacheFileName, userSession)
        print('User profile credentials will expire: ' + str(userSession['Expiration']), file=sys.stderr)
        return userSession
    else:
        log.debug('Using cache credentials')
        print('User profile credentials will expire: ' + str(cacheSession['Expiration']), file=sys.stderr)
        return cacheSession

def get_role_credentials(arguments, configSection, userSession):
    """
    arguments - the command-line arguments passed into AWSume;
    configSection - the profile from the config file;
    userSession - the session credentials for the user calling assume_role;
    get awsume-formatted role credentials from calling assume_role with `userSession` credentials
    """
    log.info('Getting the role credentials')

    #create new client based on the new session credentials
    log.debug('Creating the role client')
    roleClient = create_boto_sts_client(None,
                                        userSession['SecretAccessKey'],
                                        userSession['AccessKeyId'],
                                        userSession['SessionToken'])
    #assume the role
    if arguments.sessionname:
        session_name = arguments.sessionname
    else:
        session_name = configSection['__name__'].replace('profile ', '') + '-awsume-session'
    awsRoleSession = get_assume_role_credentials(roleClient,
                                                 configSection['role_arn'],
                                                 session_name)

    roleSession = create_awsume_session(awsRoleSession, configSection)
    return roleSession

def start_auto_refresher(arguments, userSession, configSection, credentialsSection, out_data, credentialsPath=AWS_CREDENTIALS_FILE):
    """
    arguments - the command-line arguments passed into AWSume;
    userSession - the session credentials for the user to call assume_role with;
    configSection - the profile from the config file;
    credentialsSection - the profile from the credentials file
    """
    log.info('Starting the autoAwsume auto-refresher')

    cacheFileName = 'awsume-temp-' + credentialsSection['__name__']

    #create a profile in credentials file to store session credentials
    autoAwsumeProfileName = 'auto-refresh-' + arguments.profile_name
    write_auto_awsume_session(autoAwsumeProfileName, userSession, cacheFileName, configSection['role_arn'], credentialsPath)

    #kill all autoAwsume processes before starting a new one
    log.debug('Killing all autoAwsume processes before we start a new one')
    kill_all_auto_processes()
    auto_awsume_out_data = 'Auto' + ' ' + autoAwsumeProfileName + ' ' + str(arguments.profile_name)
    out_data.set_data(auto_awsume_out_data)

def handle_getting_role_credentials(configSection, credentialsSection, userSession, roleSession, arguments, out_data):
    """
    configSection - the profile from the config file;
    credentialsSection - the profile from the credentials file;
    userSession - the session credentials for the user to call assume_role with;
    arguments - the command-line arguments passed into AWSume;
    return the role credentials and handle any special cases
    """
    log.info('Handling getting role credentials')

    if is_role_profile(configSection):
        log.debug('The profile is a role')
        #if the user wants to auto-refresh the role credentials
        if arguments.auto_refresh is True:
            log.debug('AutoRefresh flag is up, starting autoAwsume')
            start_auto_refresher(arguments, userSession, configSection, credentialsSection, out_data)
        #do this anyway in case a plugin needs it
        log.debug('Assuming the role normally')
        roleSession = get_role_credentials(arguments, configSection, userSession)
        print('Role profile credentials will expire: ' + str(roleSession['Expiration']), file=sys.stderr)
        return roleSession
    else:
        log.debug('The profile is not a role')
        if arguments.auto_refresh is True:
            print('Using user credentials, autoAwsume will not run.', file=sys.stderr)
        return None

def validate_credentials_profile(awsumeCredentialsProfile):
    """
    awsumeCredentialsProfile - the profile to validate;
    validate that `awsumeConfigProfile` has proper aws credentials;
    if not, print an error and exit
    """
    log.info('Validating credentials profile')

    if 'aws_access_key_id' not in awsumeCredentialsProfile:
        print('AWSume Error: Your profile does not contain an access key id', file=sys.stderr)
        exit(1)
    if 'aws_secret_access_key' not in awsumeCredentialsProfile:
        print('AWSume Error: Your profile does not contain a secret access key', file=sys.stderr)
        exit(1)
    log.debug('Credentials profile is valid')

def is_role_profile(profileToCheck):
    """
    profileToCheck - the profile to check;
    return if `profileToCheck` is a role or user
    """
    log.info('Checking if the profile is a role')

    #if both 'source_profile' and 'role_arn' are in the profile, then it is a role profile
    if 'source_profile' in profileToCheck and 'role_arn' in profileToCheck:
        log.debug('Profile has both a source_profile and a role-arn')
        return True
    #if the profile has one of them, but not the other
    if 'source_profile' in profileToCheck:
        print('AWSume Error: Profile contains a source_profile, but no role_arn', file=sys.stderr)
        exit(1)
    if 'role_arn' in profileToCheck:
        print('AWSume Error: Profile contains a role_arn, but no source_profile', file=sys.stderr)
        exit(1)
    #if 'source_profile' and 'role_arn' are not in the profile, it is a user profile
    return False

def read_mfa():
    """
    prompt the user to enter an MFA code;
    return the string entered by the user
    """
    log.info('Reading MFA')

    print('Enter MFA Code: ', file=sys.stderr, end='')
    mfaToken = input()
    log.debug('Read input: ' + mfaToken)
    return mfaToken

def is_valid_mfa_token(mfaToken):
    """
    mfaToken - the token to validate;
    return if `mfaToken` is a valid MFA code
    """
    log.info('Checking if MFA is valid')
    log.debug('mfaToken=' + mfaToken)
    #compare the given token with the regex
    mfaTokenPattern = re.compile('^[0-9]{6}$')
    if not mfaTokenPattern.match(mfaToken):
        log.debug('mfaToken is not valid')
        return False
    log.debug('mfaToken is valid')
    return True

def create_boto_sts_client(profileName=None, secretAccessKey=None, accessKeyId=None, sessionToken=None):
    """
    profileName - the name of the profile to create the client with;
    secretAccessKey - secret access key that can be passed into the session;
    accessKeyId - access key id that can be passed into the session;
    sessionToken - session token that can be passed into the session;
    return a boto3 session client
    """
    log.info('Creating a Boto3 STS client')
    log.debug('profile_name=' + str(profileName))
    log.debug('aws_access_key_id=' + str(accessKeyId))
    log.debug('aws_secret_access_key=' + str(secretAccessKey))
    log.debug('aws_session_token=' + str(sessionToken))
    #establish the boto session with given credentials
    botoSession = boto3.Session(profile_name=profileName,
                                aws_access_key_id=accessKeyId,
                                aws_secret_access_key=secretAccessKey,
                                aws_session_token=sessionToken)
    #create an sts client, always defaulted to us-east-1
    return botoSession.client('sts', region_name='us-east-1')

def get_session_token_credentials(getSessionTokenClient, awsumeProfile):
    """
    getSessionTokenClient - the client to make the call on;
    awsumeProfile - an awsume-formatted profile;
    return the session token credentials
    """
    log.info('Getting the session token credentials')

    #if the profile doesn't have an mfa_serial entry,
    #mfa isn't required, so just call get_session_token
    if 'mfa_serial' not in awsumeProfile:
        log.debug('Profile does not require MFA for session token')
        return getSessionTokenClient.get_session_token()
    else:
        #get the mfa arn
        mfaSerial = awsumeProfile['mfa_serial']
        #get mfa token
        mfaToken = read_mfa()
        if not is_valid_mfa_token(mfaToken):
            print('Invalid MFA Code', file=sys.stderr)
            exit(1)
        #make the boto sts get_session_token call
        try:
            log.debug('SerialNumber=' + mfaSerial)
            log.debug('TokenCode=' + mfaToken)
            return getSessionTokenClient.get_session_token(
                SerialNumber=mfaSerial,
                TokenCode=mfaToken)

        except Exception as e:
            print('AWSume Error: ' + str(e), file=sys.stderr)
            exit(1)

def get_assume_role_credentials(assumeRoleClient, roleArn, roleSessionName):
    """
    assumeRoleClient - the client to make the sts call on;
    roleArn - the role arn to use when assuming the role;
    roleSessionName - the name to assign to the role-assumed session;
    assume role and return the session credentials
    """
    log.info('Getting the role credentials')

    try:
        log.debug('RoleArn=' + roleArn)
        log.debug('RoleSessionName=' + roleSessionName)
        return assumeRoleClient.assume_role(
            RoleArn=roleArn,
            RoleSessionName=roleSessionName)
    except Exception as e:
        print('AWSume Error: ' + str(e), file=sys.stderr)
        exit(1)

def create_awsume_session(awsCredentialsProfile, awsConfigProfile):
    """
    awsCredentialsProfile - contains the credentials required for setting the session;
    awsConfigProfile - contains the region required for setting the session;
    returns an awsume-formatted session as a dict
    """
    log.info('Creating an awsume-formatted session')

    #if the role is invalid
    if awsCredentialsProfile.get('Credentials'):
        #create the awsume session
        awsumeSession = collections.OrderedDict()
        awsumeSession['SecretAccessKey'] = awsCredentialsProfile.get('Credentials').get('SecretAccessKey')
        awsumeSession['SessionToken'] = awsCredentialsProfile.get('Credentials').get('SessionToken')
        awsumeSession['AccessKeyId'] = awsCredentialsProfile.get('Credentials').get('AccessKeyId')
        awsumeSession['region'] = awsConfigProfile.get('region')
        awsumeSession['Expiration'] = awsCredentialsProfile.get('Credentials').get('Expiration')
        #convert the time to local time
        if awsumeSession.get('Expiration'):
            if awsumeSession['Expiration'].tzinfo != None:
                awsumeSession['Expiration'] = awsumeSession['Expiration'].astimezone(dateutil.tz.tzlocal())
        return awsumeSession
    print('AWSume Error: Invalid Credentials', file=sys.stderr)
    exit(1)

def session_string(awsumeSession, arguments=None):
    """
    awsumeSession - the session to create a string out of;
    arguments - the command-line arguments;
    create a formatted and space-delimited string containing useful credential information;
    if an empty session is given, an empty string is returned
    """
    log.info('Converting the session object to a session string')
    #Get the default profile for region fallback
    if arguments:
        tempDefault = arguments.default
        #spoof default needing default profile
        arguments.default = True
        defaultProfile = get_config_profile(get_config_profile_list(arguments, None), arguments, None)
        arguments.default = tempDefault
        if not awsumeSession['region']:
            awsumeSession['region'] = defaultProfile.get('region')
    if all(cred in awsumeSession for cred in ('SecretAccessKey', 'SessionToken', 'AccessKeyId', 'region')):
        return str(awsumeSession['SecretAccessKey']) + ' ' + \
            str(awsumeSession['SessionToken']) + ' ' + \
            str(awsumeSession['AccessKeyId']) + ' ' + \
            str(awsumeSession['region'])
    return ''

def parse_session_string(sessionString):
    """
    sessionString - the formatted string that contains session credentials;
    return a session dict containing the session credentials contained in `sessionString`;
    if `sessionString` is invalid, an empty dict will be returned
    """
    log.info('Converting the session string to a session object')

    sessionArray = sessionString.split(' ')
    awsumeSession = collections.OrderedDict()
    if len(sessionArray) == 5:
        awsumeSession['SecretAccessKey'] = sessionArray[0]
        awsumeSession['SessionToken'] = sessionArray[1]
        awsumeSession['AccessKeyId'] = sessionArray[2]
        awsumeSession['region'] = sessionArray[3]
        if sessionArray[4] != 'None':
            awsumeSession['Expiration'] = datetime.datetime.strptime(sessionArray[4], '%Y-%m-%d_%H-%M-%S')
    return awsumeSession

def write_awsume_session_to_file(cacheFilePath, cacheFileName, awsumeSession):
    """
    cacheFilePath - the path to write the cache file to;
    cacheFileName - the name of the file to write;
    awsumeSession - the session to write;
    write the session to the file path
    """
    log.info('Writing session to file')

    if not os.path.exists(cacheFilePath):
        os.makedirs(cacheFilePath)
    out_file = open(cacheFilePath + cacheFileName, 'w+')
    if awsumeSession.get('Expiration'):
        out_file.write(session_string(awsumeSession) + ' ' + awsumeSession['Expiration'].strftime('%Y-%m-%d_%H-%M-%S'))
    else:
        out_file.write(session_string(awsumeSession) + ' ' + str(None))
    out_file.close()

def read_awsume_session_from_file(cacheFilePath, cacheFileName):
    """
    cacheFilePath - the path to read from;
    cacheFilename - the name of the cache file;
    return a session if the path to the file exists
    """
    log.info('Reading session from file')

    if os.path.isfile(cacheFilePath + cacheFileName):
        in_file = open(cacheFilePath + cacheFileName, 'r')
        awsumeSession = parse_session_string(in_file.read())
    else:
        log.debug('The file ' + cacheFilePath + ' does not exist')
        awsumeSession = collections.OrderedDict()
    return awsumeSession

def is_valid_awsume_session(awsumeSession):
    """
    awsumeSession - the session to validate;
    return whether or not the session is valid;
    if credentials are expired, or don't exist, they're invalid;
    else they are valid
    """
    log.info('Checking if the session is valid')

    #check if the session has an expiration
    if awsumeSession.get('Expiration'):
        #check if the session is expired
        if awsumeSession.get('Expiration') > datetime.datetime.now().replace():
            return True
        log.debug('Session is expired')
        return False
    return False

def write_auto_awsume_session(autoAwsumeName, awsumeSession, awsumeCacheFile, roleArn, awsumeCredentialsPath):
    """
    autoAwsumeName - the name of the section we are going to write;
    awsumeSession - the session we are going to write under the section;
    awsumeCacheFile - the name of the cache file for the auto-refresh to reference;
    roleArn - the auto-refresher needs this to be able to assume the role;
    add `awsumeSession` under the name `autoAwsumeName` to the credentials file;
    if the section already exists, remove and replace with the new one
    """
    log.info('Writing autoAwsume session')

    #check to see if profile exists
    autoAwsumeParser = ConfigParser.ConfigParser()
    autoAwsumeParser.read(awsumeCredentialsPath)
    for section in autoAwsumeParser._sections:
        autoAwsumeParser._sections[section]['__name__'] = section
    #if the section already exists, remove it to overwrite
    if autoAwsumeParser.has_section(autoAwsumeName):
        autoAwsumeParser.remove_section(autoAwsumeName)
    #place the new session credentials in the file
    autoAwsumeParser.add_section(autoAwsumeName)
    autoAwsumeParser.set(autoAwsumeName, 'aws_session_token', awsumeSession['SessionToken'])
    autoAwsumeParser.set(autoAwsumeName, 'aws_security_token', awsumeSession['SessionToken'])
    autoAwsumeParser.set(autoAwsumeName, 'aws_access_key_id', awsumeSession['AccessKeyId'])
    autoAwsumeParser.set(autoAwsumeName, 'aws_secret_access_key', awsumeSession['SecretAccessKey'])
    autoAwsumeParser.set(autoAwsumeName, 'awsume_cache_file', awsumeCacheFile)
    autoAwsumeParser.set(autoAwsumeName, 'aws_role_arn', roleArn)

    if awsumeSession['region'] != 'None':
        autoAwsumeParser.set(autoAwsumeName, 'region', awsumeSession['region'])
        autoAwsumeParser.set(autoAwsumeName, 'default_region', awsumeSession['region'])
    #write our changes to the file
    autoAwsumeParser.write(open(awsumeCredentialsPath, 'w'))

def kill_all_auto_processes():
    """
    kill all running autoAwsume processes
    """
    log.info('Killing all autoAwsume processes')

    for proc in psutil.process_iter():
        try:
            #kill the autoAwsume process if no more auto-refresh profiles remain
            process_command = proc.cmdline()
            for command_string in process_command:
                if 'autoAwsume' in command_string:
                    log.debug('Found an autoAwsume process, killing it')
                    #the profile and default_profile environment variables
                    proc.kill()
        except Exception:
            pass

def remove_all_auto_profiles(filePath):
    """
    remove all profiles from the credentials file that contain 'auto-refresh-'
    """
    log.info('Removing all autoAwsume profiles')

    #remove the auto-awsume profiles from the credentials file
    autoAwsumeProfileParser = ConfigParser.ConfigParser()
    autoAwsumeProfileParser.read(filePath)
    #scan all profiles to find auto-refresh profiles
    for profile in autoAwsumeProfileParser._sections:
        if 'auto-refresh-' in profile:
            log.debug('Removing profile ' + profile + ' from credentials file')
            autoAwsumeProfileParser.remove_section(profile)
    #save changes
    autoAwsumeProfileParser.write(open(filePath, 'w'))

def remove_auto_awsume_profile_by_name(profileName, filePath):
    """
    remove only the given auto-awsume profile from the credentials file
    """
    log.info('Removing an autoAwsume profile by name')

    autoAwsumeProfileParser = ConfigParser.ConfigParser()
    autoAwsumeProfileParser.read(filePath)
    #scan all profiles to find auto-refresh profiles
    for profile in autoAwsumeProfileParser._sections:
        if profile == 'auto-refresh-' + profileName:
            log.debug('Removing profile ' + profile + ' from credentials file')
            autoAwsumeProfileParser.remove_section(profile)
    #save changes
    autoAwsumeProfileParser.write(open(filePath, 'w'))

def is_auto_refresh_profiles(filePath):
    """
    return whether or not there is any auto-refresh profiles
    """
    log.info('Checking if there are autoAwsume profiles')

    autoAwsumeProfileParser = ConfigParser.ConfigParser()
    autoAwsumeProfileParser.read(filePath)

    #scan all profiles to find auto-refresh profiles
    for profile in autoAwsumeProfileParser._sections:
        if 'auto-refresh-' in profile:
            log.debug('Found an auto-refresh profile')
            return True
    return False

def stop_auto_refresh(out_data, profileName=None, filePath=AWS_CREDENTIALS_FILE):
    """
    profileName - the profile to stop auto-refreshing for;
    clean up autoAwsume's mess, kill autoAwsume, and exit
    """
    log.info('Removing all autoAwsume processes and stopping autoAwsume')
    log.debug('Profile name: ' + str(profileName))

    if profileName is None:
        log.debug('Profile name not given, deleting all autoAwsume profiles')
        remove_all_auto_profiles(filePath)
    else:
        log.debug('Profile name given, only deleting that autoAwsume profile')
        remove_auto_awsume_profile_by_name(profileName, filePath)
    #if no more auto-refresh profiles remain, kill the process
    if not is_auto_refresh_profiles(filePath):
        log.debug('There are no auto-refresh profiles remaining, killing autoAwsume')
        kill_all_auto_processes()
        kill_out_data = 'Kill'
        out_data.set_data(kill_out_data)
    else:
        stop_out_data = 'Stop ' + profileName
        out_data.set_data(stop_out_data)

def get_account_id(profile):
    """
    profile - the combined config/credentials profile;
    return the account ID of the given profile as a string
    """
    if profile.get('role_arn'):
        return profile['role_arn'].replace('arn:aws:iam::','').split(':')[0]
    if profile.get('mfa_serial'):
        return profile['mfa_serial'].replace('arn:aws:iam::','').split(':')[0]
    # return "STS: " + str(
    #   boto3.client('sts',
    #                aws_access_key_id=profile['aws_access_key_id'],
    #                aws_secret_access_key=profile['aws_secret_access_key'])
    #                .get_caller_identity()
    #                .get('Account'))
    return "Unavailable"

def generate_formatted_data(configSections, credentialsSections):
    """
    configSections - the profile from the config file;
    format the config profiles for easy printing
    """
    log.info('Generating print-friendly profile data')

    #list headers
    for section in list(configSections):
        if 'profile ' in section:
            configSections[section.replace('profile ', '')] = configSections.pop(section)

    #combine config and credentials sections
    for prof in set(configSections.keys() + credentialsSections.keys()):
        if credentialsSections.get(prof) and configSections.get(prof):
            credentialsSections[prof].update(configSections[prof])
        elif configSections.get(prof):
            credentialsSections[prof] = configSections[prof]

    credentialsSections = collections.OrderedDict(sorted(credentialsSections.items()))

    profileList = []
    profileList.append([])
    profileList[0].append('PROFILE')
    profileList[0].append('TYPE')
    profileList[0].append('SOURCE')
    profileList[0].append('MFA?')
    profileList[0].append('REGION')
    profileList[0].append('ACCOUNT')
    #now fill the tables with the appropriate data
    index = 1
    for section in credentialsSections:
        #don't add any autoAwsume profiles
        if 'auto-refresh-' not in section:
            if is_role_profile(credentialsSections[section]):
                profileList.append([])
                profileList[index].append(section.replace('profile ', ''))
                profileList[index].append('Role')
                profileList[index].append(credentialsSections[section]['source_profile'])
                profileList[index].append('Yes' if 'mfa_serial' in credentialsSections[section] else 'No')
                profileList[index].append(str(credentialsSections[section].get('region')))
                profileList[index].append(get_account_id(credentialsSections[section]))
            else:
                profileList.append([])
                profileList[index].append(section.replace('profile ', ''))
                profileList[index].append('User')
                profileList[index].append('None')
                profileList[index].append('Yes' if 'mfa_serial' in credentialsSections[section] else 'No')
                profileList[index].append(str(credentialsSections[section].get('region')))
                profileList[index].append(get_account_id(credentialsSections[section]))
            index += 1
    return profileList

def print_formatted_data(formattedProfileData):
    """
    formattedProfileData - the data to display, formatted;
    display `formattedProfileData` in a nice, proper way
    """
    log.info('Printing formatted profile data')
    print("Listing...\n")

    widths = [max(map(len, col)) for col in zip(*formattedProfileData)]
    print('AWS Profiles'.center(sum(widths) + 10, '='))
    for row in formattedProfileData:
        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

def list_profile_data(configSections, credentialsSections):
    """
    List useful information about awsume-able profiles
    """
    log.info('Listing profile data')

    formattedProfiles = generate_formatted_data(configSections, credentialsSections)
    print_formatted_data(formattedProfiles)

def list_roles_users():
    rolesUsersList = []
    configSections = get_config_profile_list(None, None)
    credentialsSections = get_credentials_profile_list(None, None)

    for profile in configSections:
        rolesUsersList.append(profile.replace('profile ', ''))
    for profile in credentialsSections:
        if 'auto-refresh-' not in profile:
            rolesUsersList.append(profile.replace('profile ', ''))
    return rolesUsersList

def register_plugins(app, manager):
    """
    app - the app to modify;
    manager - the plugin manager that contains the modifying plugins;
    register all available plugins from `manager` to `app`;
    verify that there isn't any conflicting plugins
    """
    log.info('Register plugins')

    for plugin in manager.getAllPlugins():
        # verify major versions
        try:
            if plugin.plugin_object.TARGET_VERSION.split('.')[0] != __version__.split('.')[0]:
                print("AWSume Warning: [" + str(plugin.name) + "] Target version: " + str(plugin.plugin_object.TARGET_VERSION) + ", AWSume version: " + __version__, file=sys.stderr)
        except AttributeError:
            print("AWSume Warning: [" + str(plugin.name) + "] has no `TARGET_VERSION` attribute", file=sys.stderr)

        if 'add_arguments_func' in dir(plugin.plugin_object):
            app.register('add_arguments_func', plugin.plugin_object.add_arguments_func)
        if 'handle_arguments_func' in dir(plugin.plugin_object):
            app.register('handle_arguments_func', plugin.plugin_object.handle_arguments_func)
        if 'get_config_profile_list_func' in dir(plugin.plugin_object):
            app.register('get_config_profile_list_func', plugin.plugin_object.get_config_profile_list_func)
        if 'get_credentials_profile_list_func' in dir(plugin.plugin_object):
            app.register('get_credentials_profile_list_func', plugin.plugin_object.get_credentials_profile_list_func)
        if 'get_config_profile_func' in dir(plugin.plugin_object):
            app.register('get_config_profile_func', plugin.plugin_object.get_config_profile_func)
        if 'get_credentials_profile_func' in dir(plugin.plugin_object):
            app.register('get_credentials_profile_func', plugin.plugin_object.get_credentials_profile_func)
        if 'handle_profiles_func' in dir(plugin.plugin_object):
            app.register('handle_profiles_func', plugin.plugin_object.handle_profiles_func)
        if 'get_user_credentials_func' in dir(plugin.plugin_object):
            app.register('get_user_credentials_func', plugin.plugin_object.get_user_credentials_func)
        if 'handle_getting_role_func' in dir(plugin.plugin_object):
            app.register('handle_getting_role_func', plugin.plugin_object.handle_getting_role_func)
        if 'post_awsume_func' in dir(plugin.plugin_object):
            app.register('post_awsume_func', plugin.plugin_object.post_awsume_func)
        if 'list_roles_users_func' in dir(plugin.plugin_object):
            app.register('list_roles_users_func', plugin.plugin_object.list_roles_users_func)

def locate_plugins(manager, pluginPath):
    """
    manager - the plugin manager that will find the plugins;
    find the plugins in the `~/.aws/awsumePlugins` directory
    """
    log.info('Locating plugins')

    #make the plugin path if it doesn't exist
    if not os.path.exists(pluginPath):
        os.makedirs(pluginPath)
    manager.setPluginPlaces([pluginPath])

def create_awsume_plugin_manager(pluginPath):
    """
    create the plugin manager and register all available categories of plugins
    """
    log.info('Creating a plugin manager')

    manager = PluginManager.PluginManager()
    locate_plugins(manager, pluginPath)
    manager.collectPlugins()
    return manager


class App(object):
    """
    The app that runs AWSume
    """
    #all of the functions that AWSume will call
    add_arguments_funcs = []
    handle_arguments_funcs = []
    get_config_profile_list_funcs = []
    get_credentials_profile_list_funcs = []
    get_config_profile_funcs = []
    get_credentials_profile_funcs = []
    handle_profiles_funcs = []
    get_user_credentials_funcs = []
    handle_getting_role_funcs = []
    post_awsume_funcs = []
    list_roles_users_funcs = []

    def __init__(self):
        """
        Set the default functions, they may be overwritten with the register function
        """
        self.add_arguments_funcs.append(add_arguments)
        self.handle_arguments_funcs.append(handle_command_line_arguments)
        self.get_config_profile_list_funcs.append(get_config_profile_list)
        self.get_credentials_profile_list_funcs.append(get_credentials_profile_list)
        self.get_config_profile_funcs.append(get_config_profile)
        self.get_credentials_profile_funcs.append(get_credentials_profile)
        self.handle_profiles_funcs.append(handle_profiles)
        self.get_user_credentials_funcs.append(get_user_credentials)
        self.handle_getting_role_funcs.append(handle_getting_role_credentials)
        self.list_roles_users_funcs.append(list_roles_users)

    def register(self, functionType, newFunction):
        """
        functionType - the name of the function to overwrite;
        newFunction - the function to overwrite with;
        Set the App's function `functionType` to the `newFunction`
        """
        if functionType == 'add_arguments_func':
            self.add_arguments_funcs.append(newFunction)
        elif functionType == 'handle_arguments_func':
            self.handle_arguments_funcs.append(newFunction)
        elif functionType == 'get_config_profile_list_func':
            self.get_config_profile_list_funcs.append(newFunction)
        elif functionType == 'get_credentials_profile_list_func':
            self.get_credentials_profile_list_funcs.append(newFunction)
        elif functionType == 'get_config_profile_func':
            self.get_config_profile_funcs.append(newFunction)
        elif functionType == 'get_credentials_profile_func':
            self.get_credentials_profile_funcs.append(newFunction)
        elif functionType == 'handle_profiles_func':
            self.handle_profiles_funcs.append(newFunction)
        elif functionType == 'get_user_credentials_func':
            self.get_user_credentials_funcs.append(newFunction)
        elif functionType == 'handle_getting_role_func':
            self.handle_getting_role_funcs.append(newFunction)
        elif functionType == 'post_awsume_func':
            self.post_awsume_funcs.append(newFunction)
        elif functionType == 'list_roles_users_func':
            self.list_roles_users_funcs.append(newFunction)

    def run(self):
        """
        Execute AWSume
        """
        #object for sending data to the shell scripts
        out_data = OutData()
        atexit.register(out_data.print_data)

        #parse command-line arguments
        awsumeArgParser = generate_awsume_argument_parser()
        for func in self.add_arguments_funcs:
            func(awsumeArgParser)
        commandLineArguments = parse_arguments(awsumeArgParser, sys.argv[1:])

        #handle arguments
        for func in self.handle_arguments_funcs:
            func(commandLineArguments, self, out_data)

        #get the list of config profiles
        log.debug("Getting a list of config profiles")
        configProfileList = collections.OrderedDict()
        for func in self.get_config_profile_list_funcs:
            configProfileList.update(func(commandLineArguments, out_data, AWS_CONFIG_FILE))
        log.debug("Config profile list:\n" + json.dumps(configProfileList, indent=4))

        #get the list of credentials profiles
        log.debug("Getting a list of credentials profiles")
        credentialsProfileList = collections.OrderedDict()
        for func in self.get_credentials_profile_list_funcs:
            credentialsProfileList.update(func(commandLineArguments, out_data, AWS_CREDENTIALS_FILE))
        log.debug("Credentials profile list:\n" + json.dumps(credentialsProfileList, indent=4))

        #get the config profiles
        log.debug("Getting the config profile")
        configProfile = None
        for func in self.get_config_profile_funcs:
            if not configProfile:
                configProfile = func(configProfileList, commandLineArguments, out_data)
        log.debug("Config profile:\n" + json.dumps(configProfile, indent=4))

        #get the credentials profile
        log.debug("Getting the credentials profile")
        credentialsProfile = None
        for func in self.get_credentials_profile_funcs:
            if not credentialsProfile:
                credentialsProfile = func(credentialsProfileList, configProfile, commandLineArguments, out_data, AWS_CREDENTIALS_FILE)
        log.debug("Credentials profile:\n" + json.dumps(credentialsProfile, indent=4))

        #handle those profiles
        for func in self.handle_profiles_funcs:
            func(configProfile, credentialsProfile, commandLineArguments, out_data)

        #now we have to get the session token
        log.debug("Getting users session")
        awsumeUserSession = None
        for func in self.get_user_credentials_funcs:
            awsumeUserSession = func(configProfile, credentialsProfile, awsumeUserSession, AWS_CACHE_DIRECTORY, commandLineArguments, out_data)
        sessionToUse = awsumeUserSession
        log.debug("User session:\n" + json.dumps(awsumeUserSession, default=logDatetimeConverter, indent=4))

        #assume the role
        log.debug("Getting the role session")
        awsumeRoleSession = None
        for func in self.handle_getting_role_funcs:
            awsumeRoleSession = func(configProfile, credentialsProfile, awsumeUserSession, awsumeRoleSession, commandLineArguments, out_data)
        log.debug("Role session:\n" + json.dumps(awsumeRoleSession, indent=4, default=logDatetimeConverter))

        #if the role session is valid
        if awsumeRoleSession:
            sessionToUse = awsumeRoleSession
        log.debug("Session we're going to use:\n" + json.dumps(sessionToUse, indent=4, default=logDatetimeConverter))

        #post AWSume functions
        log.debug("Running post-awsume operations")
        for func in self.post_awsume_funcs:
            func(configProfileList, credentialsProfileList, configProfile, credentialsProfile, sessionToUse, commandLineArguments, out_data)

        #send shell script wrapper the session environment variables
        log.debug("Sending data to shell wrappers")
        awsume_out_data = 'Awsume' + ' ' + session_string(sessionToUse, commandLineArguments) + ' ' + str(commandLineArguments.profile_name)
        out_data.set_data(awsume_out_data)

def main():
    #create the plugin manager
    pluginManager = create_awsume_plugin_manager(HOME_PATH + '/.aws/awsumePlugins/')
    #create AWSume
    awsumeApp = App()
    #hook up the plugins
    register_plugins(awsumeApp, pluginManager)
    #run AWSume
    awsumeApp.run()

if __name__ == '__main__':
    main()
