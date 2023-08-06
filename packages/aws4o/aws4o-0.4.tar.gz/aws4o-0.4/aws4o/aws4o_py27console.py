#!/usr/bin/python

def console() : 

    import re
    import sys
    import boto3
    import base64
    import logging
    import getpass
    import requests
    import ConfigParser
    import xml.etree.ElementTree as ET

    from bs4 import BeautifulSoup
    from os.path import expanduser
    # from urlparse import urlparse, urlunparse
    from datetime import datetime as dt
    from datetime import timedelta as td
    from cookielib import CookieJar

    ##########################################################################
    # Variables

    # region: The default AWS region that this script will connect
    # to for all API calls
    region = 'us-west-2'

    # output format: The AWS CLI output format that will be configured in the
    # saml profile (affects subsequent CLI calls)
    outputformat = 'json'

    # awsconfigfile: The file where this script will store the temp
    # credentials under the saml profile
    awsconfigfile = '/.aws/credentials'

    # SSL certificate verification: Whether or not strict certificate
    # verification is done, False should only be used for dev/test
    sslverification = True

    # idpentryurl: The initial url that starts the authentication process.
    idpentryurl = 'https://idp.stanford.edu/idp/profile/SAML2/Unsolicited/SSO?providerId=urn:amazon:webservices'

    # Uncomment to enable low level debugging
    #logging.basicConfig(level=logging.DEBUG)

    ##########################################################################
    
    # Get the federated credentials from the user
    print( "  Username:" ),
    username = raw_input()
    password = getpass.getpass( "  Password: " )
    print( " " )

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
    formsoup = BeautifulSoup( formresponse.text.decode('utf8') , "html.parser" )

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
    soup , assertion = BeautifulSoup( response.text.decode('utf8') , "html.parser" ) , ''

    # Look for the SAMLResponse attribute of the input tag (determined by analyzing the debug print lines above)
    for inputtag in soup.find_all( 'input' ): 
        if( inputtag.get('name') == 'SAMLResponse' ) :
            #print(inputtag.get('value'))
            assertion = inputtag.get('value')

    # Better error handling is required for production use.
    if ( assertion == '' ) :

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
                soup , assertion = BeautifulSoup( response.text.decode('utf8') , "html.parser" ) , ''

                # Look for the SAMLResponse attribute of the input tag
                for inputtag in soup.find_all( 'input' ): 
                    if( inputtag.get('name') == 'SAMLResponse' ) :
                        assertion = inputtag.get('value')
                        # print( assertion )

    # Better error handling is required for production use.
    if ( assertion == '' ) :
        print( "  Response did not contain a valid SAML assertion. For support, email gsb_circle_research@stanford.edu" )
        print( " " )
        print( "------------------------------------------------------------------------------------------" )
        print( " " )
        sys.exit(0)
    #else : 
    #    print assertion

    # Parse the returned assertion and extract the authorized roles
    awsroles = []
    root = ET.fromstring( base64.b64decode(assertion) )

    # print( base64.b64decode(assertion) )

    # from xml.dom import minidom
    # print minidom.parseString( ET.tostring( root ) ).toprettyxml(indent="   ")

    for saml2attribute in root.iter( '{urn:oasis:names:tc:SAML:2.0:assertion}Attribute' ):
        if ( saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role' ):
            for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                awsroles.append( saml2attributevalue.text )

    # Note the format of the attribute value should be role_arn,principal_arn
    # but lots of blogs list it as principal_arn,role_arn so let's reverse
    # them if needed
    for awsrole in awsroles:
        chunks = awsrole.split(',')
        if'saml-provider' in chunks[0]:
            newawsrole = chunks[1] + ',' + chunks[0]
            index = awsroles.index(awsrole)
            awsroles.insert(index, newawsrole)
            awsroles.remove(awsrole)

    for i in range(0,len(awsroles)) : 
        tmp = { 'RoleArn' : awsroles[i].split(',')[0] , 'PrincipalArn' : awsroles[i].split(',')[1] }
        awsroles[i] = dict( tmp ); # asserts a copy operation

    # If I have more than one role, ask the user which one they want,
    # otherwise just proceed
    print( " " )
    print( "------------------------------------------------------------------------------------------" )
    print( " " )
    if len(awsroles) > 1:
        i = 0
        print( "  Please choose the AWS role you would like to assume:" )
        print( " " )
        for awsrole in awsroles:
            print( "  [%i]: %s" % (i,awsrole['RoleArn']) )
            i += 1
        elected_role = int( input( "\n  Selection: " ) )

        # Basic sanity check of input
        if elected_role > (len(awsroles) - 1):
            print( "  You selected an invalid role index, please try again" )
            sys.exit(0)

    else:
        elected_role = 0

    role_arn = awsroles[elected_role]['RoleArn']
    principal_arn = awsroles[elected_role]['PrincipalArn']

    # "sensible" name of the role
    newrole = role_arn.split('/')[-1]

    # We will write the AWS STS token into the AWS credential file
    home = expanduser("~")
    filename = home + awsconfigfile
    
    # Read in the existing config file
    config = ConfigParser.RawConfigParser()
    config.read( filename )

    # Should we check the config (credentials) file to see if there is a
    # section for the selected role (via the for_role field)? And if the
    # section already has valid credentials?

    print( " " )
    print( "  CLI profile name (default is \"%s-ssso\"): " % newrole ),
    profilename = raw_input()

    if( profilename == "" ) :
        profilename = "%s-ssso" % newrole

    if config.has_section( profilename ) :
        if config.has_option( profilename , 'for_role' ) :
            existingrole = config.get( profilename , 'for_role' )
            if( existingrole != newrole ) :
                # NEED TO ALSO CHECK CREDENTIAL VALIDITY WITH valid_until TIME...
                if config.has_option( profilename , 'valid_until' ) :
                    validuntil = ( dt.strptime( config.get( profilename , 'valid_until' ) , "%Y-%m-%dT%H:%M:%SZ" ) - td(hours=8) )
                    pacificnow = dt.now() - td(hours=8)
                    if ( validuntil > pacificnow ) :
                        print( "  WARNING: Continuing will overwrite existing, valid credentials for the role %s." % existingrole )
                        print( "           This action could break any ongoing jobs using these credentials." )
                        print( " " )
                        print( "  Continue (y/n)? " ),
                        c = raw_input()
                        if( c == 'n' or c == 'N' ) :
                            print( " " )
                            print( "------------------------------------------------------------------------------------------" )
                            print( " " )
                            sys.exit(0)
                else :
                    print( "  WARNING: Continuing will overwrite existing credentials for the role %s." % existingrole )
                    print( "           This action could break any ongoing jobs using these credentials." )
                    print( " " )
                    print( "  Continue (y/n)? " ),
                    c = raw_input()
                    if( c == 'n' or c == 'N' ) :
                        print( " " )
                        print( "------------------------------------------------------------------------------------------" )
                        print( " " )
                        sys.exit(0)

    # Use the assertion to get an AWS STS token using Assume Role with SAML
    # conn  = boto.sts.connect_to_region( region )
    # token = conn.assume_role_with_saml( role_arn , principal_arn , assertion )
    
    stsclient = boto3.client('sts')
    response = stsclient.assume_role_with_saml( RoleArn=awsroles[elected_role]['RoleArn'] , \
                                                PrincipalArn=awsroles[elected_role]['PrincipalArn'] , \
                                                SAMLAssertion=assertion )

    # expiration time, shifted back 8 hours for Pacific time zone
    expires = ( response['Credentials']['Expiration'] - td(hours=8) )

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if not config.has_section( profilename ) :
        config.add_section( profilename )
    config.set( profilename , 'output', outputformat )
    config.set( profilename , 'region', region )
    config.set( profilename , 'aws_access_key_id', response['Credentials']['AccessKeyId'] )
    config.set( profilename , 'aws_secret_access_key', response['Credentials']['SecretAccessKey'] )
    config.set( profilename , 'aws_session_token', response['Credentials']['SessionToken'] )
    config.set( profilename , 'for_role', newrole )
    config.set( profilename , 'valid_until', expires.strftime( "%c" ) )

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write( configfile )

    # Give the user some basic info as to what has just happened

    print( "\n----------------------------------------------------------------" )
    print( " " )
    print( "  Your new access key pair has been stored in the AWS configuration file " )
    print( " " )
    print( "        %s" % filename )
    print( " " )
    print( "  under the \"%s\" profile. Note that it will expire at %s." % ( profilename , expires.strftime( "%c" ) ) )
    print( " " )
    print( "  After this time, you may safely rerun this script to refresh your access key pair." )
    print( " " )
    print( "  To use this credential call the AWS CLI with the --profile option, as in " )
    print( " " )
    print( "        aws --profile %s ec2 describe-instances" % profilename )
    print( " " )
    print( "  To report problems or errors, email gsb_circle_research@stanford.edu." )
    print( " " )
    print( "----------------------------------------------------------------\n\n" )


if __name__ == "__main__" : 
    console()
