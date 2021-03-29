import aws_cdk.aws_wafv2 as waf
from aws_cdk import core
from demo_app import DemoApp


class Waf2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Demo app with an ALB, which only allows traffic from the specified set of CIDRs
        app = DemoApp(self, 'DemoApp', allow_from_cidrs=['0.0.0.0/0'])

        ###
        # Example of adding a Web ACL with a custom rule to the load balancer of a demo app
        ###
        acl = waf.CfnWebACL

        custom_rule = acl.RuleProperty(
            name='BlockQueriesContainingSubString',
            priority=1,
            action=acl.RuleActionProperty(block={}),
            statement=acl.StatementOneProperty(
                byte_match_statement=acl.ByteMatchStatementProperty(
                    search_string='blockme',
                    field_to_match=acl.FieldToMatchProperty(query_string={}),
                    positional_constraint='CONTAINS',
                    text_transformations=[
                        acl.TextTransformationProperty(priority=0, type='NONE'),
                    ],
                )
            ),
            visibility_config=acl.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                sampled_requests_enabled=True,
                metric_name='custom_rule',
            )
        )

        # Check out the following for examples using managed rules (shield advanced)
        # https://web.archive.org/web/20210321152739/https://dev.to/vumdao/using-aws-waf-and-shield-to-protect-ddos-5d03

        # Create the ACL
        web_acl = waf.CfnWebACL(
            self, 'WebACL',
            default_action=acl.DefaultActionProperty(allow={}),
            scope='REGIONAL',  # or use CLOUDFRONT if protecting a distribution
            visibility_config=acl.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name='webACL',
                sampled_requests_enabled=True
            ),
            name=f'test-acl',
            rules=[
                custom_rule,
            ]
        )

        # Associate the ACL with a resource; Here the ALB for the demo app.
        waf.CfnWebACLAssociation(self, 'WafAclAssociationALB',
            web_acl_arn=web_acl.attr_arn,
            resource_arn=app.alb.load_balancer_arn,
        )

        # Link that triggers a block, and another to the AWS Console showing the generated WebACL
        core.CfnOutput(self, 'BlockedExampleUrl', value='http://{}/?blockme'.format(app.alb.load_balancer_dns_name))
        core.CfnOutput(self, 'AclConsoleUrl', value='https://console.aws.amazon.com/wafv2/homev2/web-acls?region={}'.format(
            core.Stack.of(self).region
        ))
