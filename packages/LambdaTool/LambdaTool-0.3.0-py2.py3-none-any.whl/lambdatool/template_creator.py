from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO
from parts import get_the_api_chunk
import os
import sys
import logging


snsTopicARN = 'snstopicarn'
trustedService = 'trustedservice'
schedule = 'scheduleexpression'
service = 'service'
new_line = '\n'
spacer = '          '

sns_topic_arn = """  snsTopicARN:
    Description: the ARN of the topic to which we are subscribing
    Type: String"""

trusted_service = """  trustedService:
    Description: service which this lambda trusts
    Type: String"""

schedule_expression = """  scheduleExpression:
    Description: rate or cron expression for a scheduled  lambda
    Type: String"""

sns_subcription_resource = """  TopicSubscription:
    Type: AWS::SNS::Subscription
    DependsOn: LambdaFunction
    Properties:
      Endpoint:
        Fn::GetAtt: [LambdaFunction, Arn]
      Protocol: lambda
      TopicArn:
        Ref: snsTopicARN
  TopicPermission:
    Type: AWS::Lambda::Permission
    DependsOn: TopicSubscription
    Properties:
      FunctionName:
        Fn::GetAtt: [LambdaFunction, Arn]
      Action: lambda:InvokeFunction
      Principal: sns.amazonaws.com"""

trusted_service_resource = """  TrustedService:
    Type: AWS::Lambda::Permission
    DependsOn: LambdaFunction
    Properties:
      FunctionName:
        Fn::GetAtt: [LambdaFunction, Arn]
      Action: lambda:InvokeFunction
      Principal:
        Ref: trustedService"""

rule_id = '{}-{}'.format(
    os.environ.get('LAMBDA_NAME', 'unknown'),
    os.environ.get('ENVIRONMENT', 'none')
)

schedule_resource = """  LambdaSchedule:
    Type: AWS::Events::Rule
    DependsOn: LambdaFunction
    Properties:
      Description: String
      ScheduleExpression:
          Ref: scheduleExpression
      State: ENABLED
      Targets:
        -
          Arn:
            Fn::GetAtt: [LambdaFunction, Arn]
          Id:
            {}
  EventPermission:
    Type: AWS::Lambda::Permission
    DependsOn: LambdaFunction
    Properties:
      FunctionName:
        Fn::GetAtt: [LambdaFunction, Arn]
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com""".format(rule_id)


class TemplateCreator:
    _stack_properties = None
    _input_file = None
    _output_file = None
    _template_file = None
    _sns_topic_arn_found = False
    _trusted_service_found = False
    _create_service = False
    _schedule_found = False
    _regio = None
    _stage_name = None
    _short_name = None
    _account = None
    _ssm_client = None
    SSM = '[ssm:'

    _food = """      Environment:
        Variables:
"""

    def __init__(self, ssm_client):
        self._ssm_client = ssm_client

    def _prop_to_yaml(self, thing):
        idx = thing.find('=')
        if idx > -1:
            key = thing[:idx]
            val = thing[(idx+1):].strip()
            val = self._get_ssm_parameter(val)
            if val:
                return key, val

        return None, None

    def _inject_stuff(self):
        try:
            with open(self._input_file, 'r') as infile:
                for thing in infile:
                    key, val = self._prop_to_yaml(thing.strip())
                    if key and val:
                        self._food += spacer + key + ': ' + val + '\n'

            buf = StringIO()
            t = Template(filename=self._template_file)

            if self._sns_topic_arn_found:
                sns_var_bits = sns_topic_arn
                sns_resource_bits = sns_subcription_resource
            else:
                sns_var_bits = ''
                sns_resource_bits = ''

            if self._trusted_service_found:
                trusted_service_var_bits = trusted_service
                trusted_service_resource_bits = trusted_service_resource
            else:
                trusted_service_var_bits = ''
                trusted_service_resource_bits = ''

            if self._schedule_found:
                schedule_var_bits = schedule_expression
                schedule_resource_bits = schedule_resource
            else:
                schedule_var_bits = ''
                schedule_resource_bits = ''

            if self._create_service:
                the_api_bits = get_the_api_chunk(
                    region=self._region,
                    stage_name=self._stage_name,
                    short_name=self._short_name,
                    account=self._account
                )
            else:
                the_api_bits = ''

            ctx = Context(
                buf,
                environment_section=self._food,
                snsTopicARN=sns_var_bits,
                snsSubscriptionResource=sns_resource_bits,
                trustedService=trusted_service_var_bits,
                trustedServiceResource=trusted_service_resource_bits,
                scheduleExpression=schedule_var_bits,
                scheduleResource=schedule_resource_bits,
                theAPI=the_api_bits
            )

            t.render_context(ctx)
            logging.info('writing template {}'.format(self._output_file))
            with open(self._output_file, "w") as outfile:
                    outfile.write(buf.getvalue())
        except Exception as wtf:
            logging.error('Exception caught in inject_stuff(): {}'.format(wtf))
            sys.exit(1)

    def _read_stack_properties(self):
        try:
            lowered_stack_properties = {}
            for key in self._stack_properties:
                lowered_key = key.lower()
                lowered_stack_properties[lowered_key] = self._stack_properties[key]

            if snsTopicARN in lowered_stack_properties:
                self._sns_topic_arn_found = True

            if trustedService in lowered_stack_properties:
                self._trusted_service_found = True

            if schedule in lowered_stack_properties:
                self._schedule_found = True

            tmp = lowered_stack_properties.get(service, 'false').lower()
            if tmp == 'true':
                self._create_service = True
        except Exception as wtf:
            logging.error('Exception caught in read_stack_properties(): {}'.format(wtf))
            sys.exit(1)

        return True

    def create_template(self, **kwargs):
        try:
            self._input_file = kwargs['function_properties']
            self._stack_properties = kwargs['stack_properties']
            self._output_file = kwargs['output_file']
            self._template_file = kwargs['template_file']
            self._region = kwargs['region']
            self._stage_name = kwargs['stage_name']
            self._short_name = kwargs['short_name']
            self._account = kwargs['account']

            self._read_stack_properties()
            self._inject_stuff()
            return True
        except Exception as wtf:
            logging.error(wtf)
            return False

    def _get_ssm_parameter(self, p):
        """
        Get parameters from Simple Systems Manager

        Args:
            p - a parameter name

        Returns:
            a value, decrypted if needed, if successful or None if things go
            sideways.
        """
        val = None
        secure_string = False
        try:
            if p.startswith(self.SSM) and p.endswith(']'):
                parts = p.split(':')
                p = parts[1].replace(']', '')
            else:
                return p

            response = self._ssm_client.describe_parameters(
                Filters=[{'Key': 'Name', 'Values': [p]}]
            )

            if 'Parameters' in response:
                t = response['Parameters'][0].get('Type', None)
                if t == 'String':
                    secure_string = False
                elif t == 'SecureString':
                    secure_string = True

                response = self._ssm_client.get_parameter(Name=p, WithDecryption=secure_string)
                val = response.get('Parameter', {}).get('Value', None)
        except Exception:
            pass

        return val


if __name__ == '__main__':
    templateCreator = TemplateCreator()
    templateCreator.create_template(
        function_properties='/tmp/scratch/f315ee80/config/dev/function.properties',
        stack_properties='/tmp/scratch/f315ee80/stack.properties',
        output_file='/tmp/template.yaml',
        template_file='template_template'
    )
