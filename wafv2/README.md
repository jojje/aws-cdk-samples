
# Example of how WAFv2 rules can be managed using CDK

This example sets up a single instance with a demo app (nginx base-install), controlled by
an ASG and surfaced using an ALB. It then adds a custom WAF-rule which blocks traffic using
WAF if a query parameter named `blockme` is found in a request to the ALB.

After deployment, a few handy URLs will be provided in the Cloudformation/CDK output, which
allows you to experiment with the WAF behavior, and poke around in the WAF console for the
generated WebACL.

The source code contains a mention of further resource / example to explore if you are
interested in incorporating managed rules as well.

The code of interest showing how to work with WAFv2 rules is found in
[waf2/waf2_stack.py][1]

## Setup
1. Make sure you have [node.js][2] installed, since AWS Cloud Development Kit requires it regardless
   of language you then elect to use for writing your stacks and constructs.
    ```
    npm install -g aws-cdk
    ```

2. Create a python3 virtualenv which will contain the python specific dependencies in your workspace.
    ```
    $ python3 -m venv .venv
    ```

3.  After the init process completes and the virtualenv is created, you can use the following
    step to activate your virtualenv on MacOS/Linux.

    ```
    $ source .venv/bin/activate
    ```

    If you are a Windows platform, you would activate the virtualenv like this:

    ```
    % .venv\Scripts\activate.bat
    ```

4.  Once the virtualenv is activated, install the required python CDK dependencies.

    ```
    $ pip install -r requirements.txt
    ```

## Usage
At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To deploy the example, issue:

```
$ cdk deploy
```

To clean up / remove the deployed resources this project generated in your AWS account, issue:

```
$ cdk destroy
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

[1]: waf2/waf2_stack.py
[2]: https://nodejs.org/en/download/

