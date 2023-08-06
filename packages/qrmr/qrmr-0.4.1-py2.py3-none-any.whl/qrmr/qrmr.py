#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   ____  _____  __  __ _____
#  / __ \|  __ \|  \/  |  __ \
# | |  | | |__) | \  / | |__) |
# | |  | |  _  /| |\/| |  _  /
# | |__| | | \ \| |  | | | \ \
#  \___\_\_|  \_\_|  |_|_|  \_\
"""
Highly opinionated Amazon Web Services (AWS) terminal login toolkit, focused on
enforcing AWS Multi-Factor Authentication (MFA).

Written in Python 3, backwards compatible with Python 2.

Currently being heavily tested in production against AWS multi-account setup (Well-Architected Framework) on macOS High Sierra.

Feels most at home using `virtualenv`, of course.

**How it works:**

* Stores your IAM User's Access and Secret Key in ``~/.qrmr/credentials.ini``
* Prompts for MFA OTP code
* Retrieves and stores fresh session token and temporary keys based on IAM User's API / SECRET keys

**Near future:**

* manage ``~/.aws/credentials`` and ``~/.aws/config`` files
* unit tests :)

Because you probably just want to start using it:

**Installation of QRMR:**

``pip install qrmr``

**Setup of AWS Credentials:**

``qrmr setup``

**Refreshing your SessionToken and temporary keys:**

``qrmr refresh``

**Be cool:**

``aws s3 ls``


**REMEMBER:** set environment variable AWS_PROFILE in your shell or virtualenv to
make life easier:

``export AWS_PROFILE=name_of_iam_user``

Find out more features by running:

``qrmr --help``

Find us on: https://gitlab.com/qrmr/qrmr

(c)Copyright 2017 - 2018, all rights reserved by QRMR / ALDG / Alexander L. de Goeij.
"""
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Python 2.7+ compatibility for e.g. macos
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import sys
import os
import logging
import argparse
import configparser
from configparser import MissingSectionHeaderError

from qrmr import __version__
#__version__ = "dev"
import colorlog
import boto3
from botocore.exceptions import ParamValidationError

# Setup logger before anything else:
logger = logging.getLogger()
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s')
)
logger = colorlog.getLogger()
logger.addHandler(handler)

# Initialize globals
USER_HOME = os.path.expanduser('~')
QRMR_HOME = USER_HOME + '/.qrmr'
QRMR_CREDENTIALS_FILE = QRMR_HOME + '/credentials.ini'
QRMR_CREDENTIALS = configparser.ConfigParser()

AWS_HOME = USER_HOME + '/.aws'
AWS_CREDENTIALS_FILE = AWS_HOME + '/credentials'
AWS_CREDENTIALS = configparser.ConfigParser()


def upgrade_qrmr():
    """Helper to install required dependencies for this script using PyPi
       (PIP).
    """
    logger.warning("Attempting upgrade of QRMR from PyPi using PIP")
    try:
        import pip
    except ImportError:
        logger.critical(
            "You do not have PyPi (PIP) installed, "
            "cannot install dependencies, go to: https://pypi.org/"
        )

    try:
        if logger.getEffectiveLevel() == logging.DEBUG:
            # Show all PIP output
            pip.main(['install', 'qrmr', '--upgrade'])
        else:
            pip.main(['install', 'qrmr', '--upgrade', '--quiet'])

        logger.info(
            "Succesfully upgraded QRMR and its dependencies to latest version.")

    except Exception as e:
        logger.warning(
            "Couldn't check or upgrade QRMR, please upgrade manually. Error: %s" % e)


def in_virtualenv():
    """Helper to check if qrmr is running in a virtualenv or venv, which can have profile defaults.

    :return: True or False.
    """
    if (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and (sys.base_prefix != sys.prefix))):
        env = os.environ["VIRTUAL_ENV"]
        logger.info(
            "You are running inside a virtualenv (or venv) named: %s" % env)
        return True   # FIXME
    else:
        logger.info(
            "You do not seem to be running inside a virtualenv (or venv)")
        return False   # FIXME


def load_credentials():
    """Loads credentials from `~/.qrmr/credentials.ini` or creates empty config
    """
    logger.debug("Attempting to load credentials from: %s" %
                 QRMR_CREDENTIALS_FILE)
    if not os.path.isfile(QRMR_CREDENTIALS_FILE):
        if not os.path.exists(QRMR_HOME):
            os.makedirs(QRMR_HOME)
        logger.warning(
            "Could not find existing '~/.qrmr/credentials.ini', creating empty one you should run setup first!"
        )

        empty_file = open(QRMR_CREDENTIALS_FILE, 'a')
        empty_file.close()
    else:
        QRMR_CREDENTIALS.read(QRMR_CREDENTIALS_FILE)
        logger.debug("Read credentials from %s and found: %s" %
                     (QRMR_CREDENTIALS_FILE, QRMR_CREDENTIALS.sections()))

    # Always reset file permissions
    os.chmod(QRMR_CREDENTIALS_FILE, 0o600)

    logger.debug("Attempting to load credentials from: %s" %
                 AWS_CREDENTIALS_FILE)
    if not os.path.isfile(AWS_CREDENTIALS_FILE):
        logger.critical(
            "Could not load AWS credentials file, investigate!")
    else:
        AWS_CREDENTIALS.read(AWS_CREDENTIALS_FILE)
        logger.debug("Read credentials from %s and found: %s" %
                     (AWS_CREDENTIALS_FILE, AWS_CREDENTIALS.sections()))

    # Always reset file permissions
    os.chmod(AWS_CREDENTIALS_FILE, 0o600)


def list_credentials(args):
    """List all configured AWS credentials available to QRMR.
    """
    logger.debug("Attempting to list all available credentials")

    load_credentials()

    for i in QRMR_CREDENTIALS.sections():
        for j in QRMR_CREDENTIALS[i]:
            if not j == "aws_secret_access_key":
                print(j, '=', QRMR_CREDENTIALS[i][j])
            elif j == "aws_secret_access_key":
                print("aws_secret_access_key = * * * redacted * * *")


def setup_credential(args):
    """Add or update AWS credential in ~/.qrmr/credentials.ini.

    ``qrmr setup``

    Setup is either interactive using terminal prompts or using CLI arguments.
    """
    logging.debug(
        "Attempting to add or update an AWS credential to ~/.qrmr/credentials.ini.")

    load_credentials()

    if args.key == 'missing':
        # Interactive setup
        logger.debug(
            "No command-line options provided, proceeding with interactive setup.")
        input_profile = str(input(
            "User Name of your AWS IAM User: "))
        input_region = str(
            input("Default AWS Region [eu-west-1]: ")) or "eu-west-1"
        input_key = str(
            input("AWS IAM User's Access Key ID: "))
        input_secret = str(
            input("AWS IAM User's Secret Access Key: "))
        input_mfa_arn = str(
            input("AWS IAM User's MFA device ARN: "))
        input_role_arn = str(
            input("AWS IAM common cross-account Role ARN for your user (optional) [blank]: ")) or "blank"
        input_duration_seconds = str(
            input("AWS Session Token duration (in seconds) [14400]: ")) or 14400

        QRMR_CREDENTIALS[input_profile] = {
            "source_profile": input_profile,
            "output": "json",   # FIXME
            "region": input_region,
            "aws_access_key_id": input_key,
            "aws_secret_access_key": input_secret,
            "mfa_arn": input_mfa_arn,
            "role_arn": input_role_arn,
            "duration_seconds": input_duration_seconds
        }

        # Store new / updated global configuration
        with open(QRMR_CREDENTIALS_FILE, 'w') as new_config_file:
            QRMR_CREDENTIALS.write(new_config_file)

    else:
        # Non-interactive setup
        logger.debug("Attempting non-interactive setup")

    load_credentials()


def refresh_token(args):
    """Refreshes AWS Session Token and temporary session keys.

    ``qrmr refresh``

    Uses AWS IAM credentials previously setup in QRMR to request a fresh SessionToken,
    temporary AccessKeyId and temporary SecretAccessKey using AWS STS.

    The time-out duration of the SessionToken is by default set to 14400 seconds,
    unless specified otherwise in ~/.qrmr/credentials.ini.

    QRMR will look at:
    * AWS_PROFILE environment variable
    * top-most credential in ``~/.qrmr/credentials``
    * ``--profile`` command-line argument

    to determine for which AWS credential to refresh the SessionToken and keys.

    Top Tip: add ``export AWS_PROFILE=name_of_iam_user`` to your ``.bashrc``, ``.zshrc`` or 
    ``virtualenv_name/bin/postactivate`` to simplify session token refresh.

    See: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html
    """
    logger.debug(
        "Attempting refresh of AWS Session Token and updating AWS credentials file.")

    load_credentials()

    profile = ""

    if args.profile:
        logger.debug("Received --profile or -p, will only refresh that one.")
        profile = args.profile
    else:
        if 'AWS_PROFILE' in os.environ:
            profile = str(os.environ["AWS_PROFILE"])
            if profile in QRMR_CREDENTIALS.sections():
                logger.info(
                    "Matching QRMR credential found for AWS_PROFILE environment variable, requesting session token as: %s" % profile)
            else:
                logger.critical(
                    "Profile specified in AWS_PROFILE environment variable (%s) not found in QRMR credentials, please add valid QRMR credential using `qrmr setup` or `unset AWS_PROFILE`." % profile)
                sys.exit(1)
        else:
            logger.warning(
                "You did not provide a specific profile using --profile or -p, currently this only works if you have only one (1) single credential set up, because we will take the first in the file. You can `export AWS_PROFILE=profile_name` to make this smart.")
            try:
                profile = str(list(QRMR_CREDENTIALS.sections())[0])
                logger.info("Requesting session token as: %s" % profile)
            except IndexError as e:
                logger.critical(
                    "Could not find a valid profile in ~/.qrmr/credentials.ini, did you run `qrmr setup`?")
                sys.exit(1)

    client = boto3.client(
        'sts',
        aws_access_key_id=QRMR_CREDENTIALS[profile]["aws_access_key_id"],
        aws_secret_access_key=QRMR_CREDENTIALS[profile]["aws_secret_access_key"]
    )

    try:
        logger.debug("Requesting Session Token for MFA: %s" %
                     QRMR_CREDENTIALS[profile]["mfa_arn"])
        mfa_token = str(input('Please provide valid AWS MFA token: '))
    except KeyboardInterrupt as e:
        logger.critical("User terminated operations")

    # Retrieve temporary credentials and fresh session token
    try:
        logging.debug("Attempting boto3 get_session_token...")
        response = client.get_session_token(
            DurationSeconds=max(
                int(QRMR_CREDENTIALS[profile]["duration_seconds"]), (60 * 60 * 24)),
            SerialNumber=QRMR_CREDENTIALS[profile]["mfa_arn"],
            TokenCode=mfa_token
        )
        logger.debug("Received Session Token response: %s" % response)
    except ParamValidationError as e:
        logger.error(
            "Could not retrieve Session Token, your config is probably malformed, try to run setup again. Error details: %s" % e)
        sys.exit(1)

    # Store temporary credentials in AWS credentials file (overwriting static keys)
    AWS_CREDENTIALS[profile] = {
        "output": QRMR_CREDENTIALS[profile]["output"],
        "region": QRMR_CREDENTIALS[profile]["region"],
        "aws_access_key_id": str(response["Credentials"]["AccessKeyId"]),
        "aws_secret_access_key": str(response["Credentials"]["SecretAccessKey"]),
        "aws_session_token": str(response["Credentials"]["SessionToken"])
    }
    # Store new / updated configuration
    with open(AWS_CREDENTIALS_FILE, 'w') as new_credentials_file:
        AWS_CREDENTIALS.write(new_credentials_file)

    logger.info(
        "AWS SessionToken and temporary keys succesfully updated in ~/.aws/credentials.")

    logger.info(
        "Top tip: add `export AWS_PROFILE=%s` to your .bashrc, .zshrc or virtualenv_name/bin/postactivate to simplify session token refresh." % profile)

    load_credentials()


def main():
    """Main handler.
    """
    parser = argparse.ArgumentParser(
        prog="qrmr",
        description=("\n   ____  _____  __  __ _____  \
                    \n  / __ \|  __ \|  \/  |  __ \  \
                    \n | |  | | |__) | \  / | |__) | \
                    \n | |  | |  _  /| |\/| |  _  /  \
                    \n | |__| | | \ \| |  | | | \ \  \
                    \n  \___\_\_|  \_\_|  |_|_|  \_\ %s \
                    \n \
                    \nCommand line utility to make working with AWS awesome.\n" % __version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Find us on: https://qrmr.io\n \
                \nInstalled version: %s \n \
                \n(c)Copyright 2017 - 2018, all rights reserved by QRMR / ALDG / Alexander L. de Goeij. \nSee LICENSE file for details."
        % __version__)

    aws_cmd_parser = argparse.ArgumentParser(add_help=False)
    aws_cmd_parser.add_argument(
        "--profile", default="missing", type=str, help="AWS Profile name (also used as source profile).")
    aws_cmd_parser.add_argument(
        "--output", default="json", type=str, help="aws cli / aws-shell default output format (default: json).")
    aws_cmd_parser.add_argument(
        "--region", default="eu-west-1", type=str, help="AWS Default Region (default: eu-west-1).")
    aws_cmd_parser.add_argument(
        "--key", default="missing", type=str, help="AWS IAM User's Access Key ID.")
    aws_cmd_parser.add_argument(
        "--secret", default="missing", type=str, help="AWS IAM User's Secret Access Key.")
    aws_cmd_parser.add_argument(
        "--role-arn", default="missing", type=str, help="AWS IAM User's Role ARN.")
    aws_cmd_parser.add_argument(
        "--mfa-arn", default="missing", type=str, help="AWS IAM User's Multi-Factor Authentication ARN.")
    aws_cmd_parser.add_argument(
        "--duration", default=(60 * 60 * 4), type=int, help="The duration, in seconds, that the credentials should remain valid (default: 4h).")

    subparsers = parser.add_subparsers()

    parser_setup = subparsers.add_parser(
        'setup',
        help="Setup new AWS IAM User credential.",
        parents=[aws_cmd_parser]
    )
    parser_setup.set_defaults(func=setup_credential)

    parser_refresh = subparsers.add_parser(
        'refresh',
        help="Refresh session tokens and temporary keys for default credential."
    )
    parser_refresh.add_argument(
        '--profile', '-p',
        help="Refresh specified profile's session token and temporary keys."
    )
    parser_refresh.add_argument(
        '--token', '-t',
        help="Provide a MFA token code as CLI option to speed up login flow."
    )
    parser_refresh.set_defaults(func=refresh_token)

    parser_list = subparsers.add_parser(
        'list',
        help="Show all available credentials.",
    )
    parser_list.set_defaults(func=list_credentials)

    parser.add_argument(
        '--version', action='version', version="%(prog)s {0}".format(__version__)
    )

    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Increase verbosity from INFO to DEBUG.',
    )

    args = parser.parse_args()

    # Optionally enable DEBUG level logging
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.info('loglevel set to: %s', logger.getEffectiveLevel())
    else:
        logger.setLevel(logging.INFO)

    logger.debug(args)

    # FIXME TODO upgrade_qrmr()

    # Call the required functions
    try:
        args.func(args)
    except AttributeError as e:
        logging.error("No valid command supplied. %s" % e)
        parser.print_help()


if __name__ == '__main__':
    main()
