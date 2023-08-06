"""Command Line Interface for Trailscraper"""
import logging
import os

import click

import trailscraper
from trailscraper import time_utils
from trailscraper.cloudtrail import load_from_dir, load_from_api
from trailscraper.policy_generator import generate_policy_from_records
from trailscraper.s3_download import download_cloudtrail_logs


@click.group()
@click.version_option(version=trailscraper.__version__)
@click.option('--verbose', default=False, is_flag=True)
def root_group(verbose):
    """A command-line tool to get valuable information out of AWS CloudTrail."""
    logger = logging.getLogger()
    if verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger('botocore').setLevel(logging.INFO)
        logging.getLogger('s3transfer').setLevel(logging.INFO)


@click.command()
@click.option('--bucket', required=True,
              help='The S3 bucket that contains cloud-trail logs')
@click.option('--prefix', default="",
              help='Prefix in the S3 bucket (including trailing slash)')
@click.option('--account-id', multiple=True, required=True,
              help='ID of the account we want to look at')
@click.option('--region', multiple=True, required=True,
              help='Regions we want to look at')
@click.option('--log-dir', default="~/.trailscraper/logs", type=click.Path(),
              help='Where to put logfiles')
@click.option('--from', 'from_s', default="one day ago", type=click.STRING,
              help='Start date, e.g. "2017-01-01" or "-1days". Defaults to "one day ago".')
@click.option('--to', 'to_s', default="now", type=click.STRING,
              help='End date, e.g. "2017-01-01" or "now". Defaults to "now".')
# pylint: disable=too-many-arguments
def download(bucket, prefix, account_id, region, log_dir, from_s, to_s):
    """Downloads CloudTrail Logs from S3."""
    log_dir = os.path.expanduser(log_dir)

    from_date = time_utils.parse_human_readable_time(from_s)
    to_date = time_utils.parse_human_readable_time(to_s)

    download_cloudtrail_logs(log_dir, bucket, prefix, account_id, region, from_date, to_date)


@click.command("generate-policy")
@click.option('--log-dir', default="~/.trailscraper/logs", type=click.Path(),
              help='Where to put logfiles')
@click.option('--filter-assumed-role-arn', multiple=True,
              help='only consider events from this role (can be used multiple times)')
@click.option('--use-cloudtrail-api', is_flag=True, default=False,
              help='Pull Events from CloudtrailAPI instead of log-dir')
@click.option('--from', 'from_s', default="one day ago", type=click.STRING,
              help='Start date, e.g. "2017-01-01" or "-1days"')
@click.option('--to', 'to_s', default="now", type=click.STRING,
              help='End date, e.g. "2017-01-01" or "now"')
def generate_policy(log_dir, filter_assumed_role_arn, use_cloudtrail_api, from_s, to_s):
    """Generates a policy that allows the events covered in the log-dir"""
    log_dir = os.path.expanduser(log_dir)
    from_date = time_utils.parse_human_readable_time(from_s)
    to_date = time_utils.parse_human_readable_time(to_s)

    if use_cloudtrail_api:
        records = load_from_api(from_date, to_date)
    else:
        records = load_from_dir(log_dir, from_date, to_date)

    policy = generate_policy_from_records(records, filter_assumed_role_arn, from_date, to_date)

    click.echo(policy.to_json())


root_group.add_command(download)
root_group.add_command(generate_policy)
