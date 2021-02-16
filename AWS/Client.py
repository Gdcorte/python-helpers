from os import environ

def set_profile_region(profile=None, region=None):
    """
        Sets the profile and region inside the environment variables so that AWS would know which credentials to use in order to access the resources.
        NOTE: When used inside an AWS environment, this should be already set by the IAM Role attached to the service. This can override the IAM role attaches or be used for local tests
    """
    if (profile):
        environ['AWS_PROFILE']=profile

    if (region):
        environ['AWS_DEFAULT_REGION']=region