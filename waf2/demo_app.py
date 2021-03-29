import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_elasticloadbalancingv2_targets as elb_targets
from aws_cdk import core
from typing import List


class DemoApp(core.Construct):
    """ Creates a simple load balanced application with an ALB in front """

    def __init__(self, scope: core.Construct, id: str, allow_from_cidrs: List[str], *, prefix=None):
        """
        allow_from_cdirs: List of CDIRs to white-list for ingress to the ALB
        """
        super().__init__(scope, id)

        vpc = ec2.Vpc(self, 'VPC',
            cidr='10.0.0.0/16',
            max_azs=2,  # At least 2 needed for ALB
            subnet_configuration=[
                ec2.SubnetConfiguration(name='Public',
                    cidr_mask=24,
                    subnet_type=ec2.SubnetType.PUBLIC)
            ])

        # Cheap nginx demo ASG with a single instance that is replaced only if terminated / failing.
        asg = autoscaling.AutoScalingGroup(self, 'ASG',
            vpc=vpc,
            instance_type=ec2.InstanceType('t2.micro'),
            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
            init=ec2.CloudFormationInit.from_elements(
                ec2.InitCommand.shell_command('amazon-linux-extras install nginx1'),
                ec2.InitCommand.shell_command('chkconfig nginx on'),
                ec2.InitCommand.shell_command('service nginx start'),
            ),
            max_capacity=1,
            min_capacity=1,
            signals=autoscaling.Signals.wait_for_all(timeout=core.Duration.minutes(3)),
            update_policy=autoscaling.UpdatePolicy.rolling_update(),
        )

        # Setup an ALB and wire it to forward traffic to the instance
        alb = elb.ApplicationLoadBalancer(self, 'ALB', vpc=vpc, internet_facing=True)
        listener = alb.add_listener('HTTP', port=80, open=False)
        listener.add_targets('Instance', port=80, targets=[asg])

        # Configure SGs
        asg.connections.allow_from(alb, ec2.Port.tcp(80), 'Allow HTTP access from ALB')
        for cidr in allow_from_cidrs:
            external = ec2.Peer.ipv4(cidr)
            alb.connections.allow_from(external, ec2.Port.tcp(80), f'Allow HTTP access from external CIDR {cidr}')

        # Inform the user of the app's (ALB's) URL
        core.CfnOutput(self, 'AlbUrl', value='http://{}/'.format(alb.load_balancer_dns_name))

        # exports for reuse
        self.vpc = vpc
        self.alb = alb