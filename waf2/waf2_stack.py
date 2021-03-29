from aws_cdk import core
from demo_app import DemoApp


class Waf2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Demo app with an ALB, which only allows traffic from the specified set of CIDRs
        app = DemoApp(self, 'DemoApp', allow_from_cidrs=['0.0.0.0/0'])

