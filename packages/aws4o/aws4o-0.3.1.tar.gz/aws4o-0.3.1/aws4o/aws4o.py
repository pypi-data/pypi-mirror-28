import os
import re
import sys
import boto3
import base64
import requests
import xml.etree.ElementTree as ET

from getpass import getpass
from bs4 import BeautifulSoup
from os.path import expanduser
# from urlparse import urlparse, urlunparse
from datetime import datetime as dt
from datetime import timedelta as td 

if(   sys.version_info[0] == 2 ) : 
    import ConfigParser
    from cookielib import CookieJar
elif( sys.version_info[0] == 3 ) : 
    from configparser import ConfigParser
    from http import cookies
else : 
    pass

from .version import __version__

class AwsConsoleSession :

    assertion   = ''
    region      = 'us-west-2'
    outputformat = 'json'
    awsroles    = []

    def __init__( self ) : 
        ver = __version__.split('.')
        r = requests.get( "https://rand.stanford.edu/software/awscli-console/VERSION" )
        if ( r.status_code == 200 ) : 
            VER = r.text.split( '.' )
            if( int(ver[0]) < int(VER[0]) ) : 
                print( "------------------------------------------------------------------------------------------" )
                print( " " )
                print( "  NOTE: major version update available. Visit https://code.stanford.edu/morrowwr/awscli-console." )
                print( " " )
                print( "------------------------------------------------------------------------------------------" )
            else : 
                if( int(ver[1]) < int(VER[1]) ) : 
                    print( "------------------------------------------------------------------------------------------" )
                    print( " " )
                    print( "  NOTE: minor version update available. Visit https://code.stanford.edu/morrowwr/awscli-console." )
                    print( " " )
                    print( "------------------------------------------------------------------------------------------" )

    def queryForLogin( self , sslverification=True , verbose=False ) : 
        if(   sys.version_info[0] == 2 ) : 
            print( "  Username:" ),
            username = raw_input()
            password = getpass.getpass( "  Password: " )
            print( " " )
            self.login( username=username , password=password , sslverification=sslverification , verbose=verbose )
        elif( sys.version_info[0] == 3 ) : 
            username = input( "  Username: " )
            password = getpass.getpass( "  Password: " )
            print( " " )
            self.login( username=username , password=password , sslverification=sslverification , verbose=verbose )
        else : 
            print( "  Sorry, the AWS CLI console tool is only currently supported on python 2 and 3." )
            return None

    def login( self , username=None , password=None , sslverification=True , verbose=False ) : 

        if( username is None ) : 
            if 'USER' in os.environ : 
                username = os.environ['USER']
                print( "Logging in as \"%s\"" % username )
            else : 
                return None

        if( password is None ) :
            password = getpass( 'Password: ' )

        # idpentryurl: The initial url that starts the authentication process.
        idpentryurl = 'https://idp.stanford.edu/idp/profile/SAML2/Unsolicited/SSO?providerId=urn:amazon:webservices'

        # Initiate session handler
        session = requests.Session()
        #print( session.cookies )

        # Programmatically get the SAML assertion
        # Opens the initial IdP url and follows all of the HTTP302 redirects, and
        # gets the resulting login page
        formresponse = session.get( idpentryurl , verify=sslverification )
        #print( session.cookies )

        # Capture the idpauthformsubmiturl, which is the final url after all the 302s
        idpauthformsubmiturl = formresponse.url

        # Parse the response and extract all the necessary values
        # in order to build a dictionary of all of the form values the IdP expects
        formsoup = BeautifulSoup( formresponse.text , "html.parser" )

        payload = {}
        for inputtag in formsoup.find_all( re.compile('(INPUT|input)') ):
            name , value = inputtag.get('name','') , inputtag.get('value','')
            if "user" in name.lower() :
                #Make an educated guess that this is the right field for the username
                payload[name] = username
            elif "email" in name.lower() :
                #Some IdPs also label the username field as 'email'
                payload[name] = username
            elif "pass" in name.lower() :
                #Make an educated guess that this is the right field for the password
                payload[name] = password
            else:
                #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
                payload[name] = value

        # Debug the parameter payload if needed
        # Use with caution since this will print sensitive output to the screen
        #print payload

        # Some IdPs don't explicitly set a form action, but if one is set we should
        # build the idpauthformsubmiturl by combining the scheme and hostname 
        # from the entry url with the form action target
        # If the action tag doesn't exist, we just stick with the 
        # idpauthformsubmiturl above
        #for inputtag in formsoup.find_all(re.compile('(FORM|form)')):
        #    action = inputtag.get('action')
        #    if action:
        #        parsedurl = urlparse(idpentryurl)
        #        idpauthformsubmiturl = parsedurl.scheme + "://" + parsedurl.netloc + action

        # *** WRM/LVG: we needed to comment this out. ***

        # Performs the submission of the IdP login form with the above post data
        response = session.post( idpauthformsubmiturl , data=payload , verify=sslverification )
        #print( session.cookies )

        # Debug the response if needed
        # print (response.text)
        idpauthformsubmiturl = response.url

        # Overwrite and delete the credential variables, just for safety
        username = '##############################################'
        password = '##############################################'
        del username
        del password

        # Decode the response and extract the SAML assertion
        soup , assertion = BeautifulSoup( response.text , "html.parser" ) , ''

        # Look for the SAMLResponse attribute of the input tag (determined by analyzing the debug print lines above)
        for inputtag in soup.find_all( 'input' ): 
            if( inputtag.get('name') == 'SAMLResponse' ) :
                #print(inputtag.get('value'))
                assertion = inputtag.get('value')

        # Better error handling is required for production use.
        if ( assertion == '' ) :

            if verbose : 
                print( "  Response did not contain a valid SAML assertion... checking for MFA..." )

            for formtag in soup.find_all( 'form' ): 

                if( formtag.get('name') == 'multifactor_send' ) :

                    payload = {}
                    for inputtag in formtag.find_all( re.compile('(INPUT|input)') ):
                        payload[ inputtag.get('name') ] = inputtag.get('value')
                    response = session.post( idpauthformsubmiturl , data=payload , verify=sslverification )
                    #print( session.cookies )

                    #with open('cookiefile', 'w') as f:
                    #    pickle.dump( requests.utils.dict_from_cookiejar(session.cookies) , f )

                    # Decode the response and extract the SAML assertion
                    soup , assertion = BeautifulSoup( response.text , "html.parser" ) , ''

                    # Look for the SAMLResponse attribute of the input tag
                    for inputtag in soup.find_all( 'input' ): 
                        if( inputtag.get('name') == 'SAMLResponse' ) :
                            assertion = inputtag.get('value')
                            # print( assertion )

        # Better error handling is required for production use.
        if ( assertion == '' ) :
            if verbose : 
                print( "  Response did not contain a valid SAML assertion. For support, email gsb_circle_research@stanford.edu" )
                print( " " )
                print( "------------------------------------------------------------------------------------------" )
                print( " " )
            return None

        # store assertion for later use
        self.assertion = assertion

        # Parse the returned assertion and extract the authorized roles
        self.awsroles = []
        root = ET.fromstring( base64.b64decode(assertion) )

        # print( base64.b64decode(assertion) )

        # from xml.dom import minidom
        # print minidom.parseString( ET.tostring( root ) ).toprettyxml(indent="   ")

        for saml2attribute in root.iter( '{urn:oasis:names:tc:SAML:2.0:assertion}Attribute' ):
            if ( saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role' ):
                for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                    self.awsroles.append( saml2attributevalue.text )

        # Note the format of the attribute value should be role_arn,principal_arn
        # but lots of blogs list it as principal_arn,role_arn so let's reverse
        # them if needed
        for awsrole in self.awsroles:
            chunks = awsrole.split(',')
            if 'saml-provider' in chunks[0]:
                newawsrole = chunks[1] + ',' + chunks[0]
                index = self.awsroles.index(awsrole)
                self.awsroles.insert(index, newawsrole)
                self.awsroles.remove(awsrole)

        self.rolenames = {}
        self.rolearns  = {}
        for i in range(0,len(self.awsroles)) :
            tmp = { 'RoleArn' : self.awsroles[i].split(',')[0] , 
                    'PrincipalArn' : self.awsroles[i].split(',')[1] }
            rolename = tmp['RoleArn'].split('/')[-1]
            tmp['RoleName'] = rolename
            self.rolenames[rolename] = i;
            self.rolearns[tmp['RoleArn']] = i;
            self.awsroles[i] = dict( tmp ); # asserts a copy operation

    def printRoles( self ) : 
        i = 0
        for awsrole in self.awsroles:
            print( "  [%i]: %s" % (i,awsrole['RoleArn']) )
            i += 1

    def getRoles( self ) : 
        return self.awsroles;

    def electRoleByIndex( self , RoleIndex , verbose=False ) : 
        if( RoleIndex > 0 and RoleIndex < len( self.awsroles ) ) : 
            self.elected_role = RoleIndex;
        else : 
            if verbose : 
                print( 'RoleIndex (%i) provided is out of range.' % RoleIndex )

    def electRoleByRoleName( self , RoleName , verbose=False ) : 
        if( RoleName in self.rolenames ) : 
            self.elected_role = self.rolenames[RoleName];
        return None

    def electRoleByRoleArn( self , RoleArn , verbose=False ) : 
        if( RoleArn in self.rolearns ) : 
            self.elected_role = self.rolearns[RoleArn];
        return None

    def getKeys( self , region="us-west-2" , outputformat="json" , verbose=False , profile=None ) :

        stsclient = boto3.client('sts')
        response = stsclient.assume_role_with_saml( RoleArn=self.awsroles[self.elected_role]['RoleArn'] , 
                                                    PrincipalArn=self.awsroles[self.elected_role]['PrincipalArn'] , 
                                                    SAMLAssertion=self.assertion )

        # expiration time, shifted back 8 hours for Pacific time zone
        expires = ( response['Credentials']['Expiration'] - td(hours=8) )
        
        if verbose : 
            print( response )
            print( expires.strftime( "%c" ) )

        # Put the credentials into a saml/role specific section instead of clobbering
        # the default credentials... 

        configfile = "%s%s" % ( expanduser('~') , '/.aws/credentials' )

        newrole = self.awsroles[self.elected_role]['RoleName']

        if profile is None : 
            profile = "%s-ssso" % newrole

        if(   sys.version_info[0] == 2 ) : 
            config = ConfigParser.RawConfigParser()
            config.read( configfile )
            if not config.has_section( profile ) :
                config.add_section( profile )
            config.set( profile , 'output', outputformat )
            config.set( profile , 'region', region )
            config.set( profile , 'aws_access_key_id', response['Credentials']['AccessKeyId'] )
            config.set( profile , 'aws_secret_access_key', response['Credentials']['SecretAccessKey'] )
            config.set( profile , 'aws_session_token', response['Credentials']['SessionToken'] )
            config.set( profile , 'for_role', newrole )
            config.set( profile , 'valid_until', expires.strftime( "%c" ) )

        elif( sys.version_info[0] == 3 ) :
            config = ConfigParser()
            config.read( configfile )
            config[profile] = {}
            config[profile]['output']                   = outputformat
            config[profile]['region']                   = region
            config[profile]['aws_access_key_id']        = response['Credentials']['AccessKeyId']
            config[profile]['aws_secret_access_key']    = response['Credentials']['SecretAccessKey']
            config[profile]['aws_session_token']        = response['Credentials']['SessionToken']
            config[profile]['for_role']                 = newrole
            config[profile]['valid_until']              = expires.strftime( "%c" )

        with open( configfile , 'w+') as f:
            config.write( f )

    def connect( self , region=None , verbose=False ) : 

        # Use the assertion to get an AWS STS token using Assume Role with SAML
        # conn  = boto.sts.connect_to_region( region )
        # token = conn.assume_role_with_saml( role_arn , principal_arn , assertion )
        
        stsclient = boto3.client('sts')
        response = stsclient.assume_role_with_saml( RoleArn=self.awsroles[self.elected_role]['RoleArn'] , 
                                                    PrincipalArn=self.awsroles[self.elected_role]['PrincipalArn'] , 
                                                    SAMLAssertion=self.assertion )
        if verbose : 
            print( response )
            print( ( response['Credentials']['Expiration'] - td(hours=8) ).strftime( "%c" ) )
            
        session = boto3.session.Session(    aws_access_key_id=response['Credentials']['AccessKeyId'] , 
                                            aws_secret_access_key=response['Credentials']['SecretAccessKey'] , 
                                            aws_session_token=response['Credentials']['SessionToken'] , 
                                            region_name=( region if region is not None else self.region ) )
        # overwrite
        response = None
        del response

        return session


