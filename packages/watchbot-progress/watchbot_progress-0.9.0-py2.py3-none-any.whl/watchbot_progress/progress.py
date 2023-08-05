from __future__ import division

import json
import logging
import os

import boto3


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class WatchbotProgress(object):
    """Sets up objects for reduce mode job tracking with SNS and DynamoDB

    The methods of this object are based on the on the equivalent
    methods in the JavaScript implementation:
    https://github.com/mapbox/watchbot-progress
    """

    def __init__(self, table_arn=None, topic_arn=None):
        # SNS Messages
        self.sns = boto3.client('sns')
        self.topic = topic_arn if topic_arn else os.environ['WorkTopic']

        # DynamoDB
        self.table_arn = table_arn if table_arn else os.environ['ProgressTable']
        if self.table_arn:
            self.table = self.table_arn.split(':table/')[-1]  # just name
        self.dynamodb = boto3.resource('dynamodb')
        self.db = self.dynamodb.Table(self.table)

    def status(self, jobid, part=None):
        """get status from dynamodb

        Parameters
        ----------
        jobid: string?
        part: optional int

        Returns
        -------
        dict, similar to JS watchbot-progress.status object
        """
        res = self.db.get_item(Key={'id': jobid}, ConsistentRead=True)
        item = res['Item']
        remaining = len(item['parts']) if 'parts' in item else 0
        percent = (item['total'] - remaining) / item['total']

        data = {'progress': percent}

        if 'error' in item:
            # failure must have a 'failed' key
            data['failed'] = item['error']
        if 'metadata' in item:
            data['metadata'] = item['metadata']
        if 'reduceSent' in item:
            data['reduceSent'] = item['reduceSent']

        if part is not None:
            # js implementation
            # if (part) response.partComplete =
            # item.parts ? item.parts.values.indexOf(part) === -1 : true;
            raise NotImplementedError()  # todo

        return data

    def set_total(self, jobid, parts):
        """ set total number of parts for the job

        Based on watchbot-progress.setTotal
        """
        total = len(parts)
        return self.db.update_item(
            Key={'id': jobid},
            ExpressionAttributeNames={
                '#p': 'parts',
                '#t': 'total'},
            ExpressionAttributeValues={
                ':p': set(range(total)),
                ':t': total},
            UpdateExpression='set #p = :p, #t = :t')

    def fail_job(self, jobid, reason):
        """fail the job, notify dynamodb

        Based on watchbot-progress.failJob
        """
        logger.error('[fail_job] {} failed because {}.'.format(jobid, reason))
        self.db.update_item(
            Key={'id': jobid},
            ExpressionAttributeNames={'#e': 'error'},
            ExpressionAttributeValues={':e': reason},
            UpdateExpression='set #e = :e')

    def complete_part(self, jobid, partid):
        """Mark part as complete

        Returns
        -------
        boolean
            Is the overall job completed yet?
        """
        res = self.db.update_item(
            Key={'id': jobid},
            ExpressionAttributeNames={'#p': 'parts'},
            ExpressionAttributeValues={':p': set([partid])},
            UpdateExpression='delete #p :p',
            ReturnValues='ALL_NEW')

        record = res['Attributes']
        if 'parts' in record and len(record['parts']) > 0:
            complete = False
        else:
            complete = True
        return complete

    def set_metadata(self, jobid, metadata):
        """Associate arbitrary metadata with a particular map-reduce job
        """
        self.db.update_item(
            Key={'id': jobid},
            ExpressionAttributeNames={'#m': 'metadata'},
            ExpressionAttributeValues={':m': metadata},
            UpdateExpression='set #m = :m')

    def send_message(self, message, subject):
        """Function wrapper to facilitate partial application"""
        return self.sns.publish(
            Message=json.dumps(message),
            Subject=subject,
            TopicArn=self.topic)
