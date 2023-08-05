"""OOP interface for S3.
"""

from cStringIO import StringIO

from owl.third.aws import common as aws_common
from owl.data import img_tools


class S3IO(aws_common.AWSService):
  """Class for managing s3 tasks.
  """
  bucket = None
  bucket_name = None

  def __init__(self, access_key, secret_key, region):
    """Create s3 client.
    """
    self.init_aws("s3", access_key, secret_key, region)

  def use_bucket(self, bucket_name):
    """Use a specified bucket.

    If the bucket doesn't exist, create one.
    """
    self.bucket = self.resource.create_bucket(Bucket=bucket_name)
    self.bucket_name = bucket_name

  def upload_img_bin(self,
                     img_bin,
                     img_format="png",
                     key_prefix="",
                     make_public=True):
    """Upload image binary data to bucket.

    Args:
      img_bin: image binary data.
      img_format: type of image, only support jpy or png.
      key_prefix: prefix of image key, used to create folders.
      make_public: whether to make it publically accessible.
    Returns:
      image object key.
    """
    assert img_format in ["png", "jpg", "jpeg"
                          ], "img_format must be either png, jpg, jpeg."
    assert self.bucket_name
    # make sure no duplicate images are saved.
    img_sha1 = img_tools.img_bin_to_sha1(img_bin)
    key_prefix = key_prefix.strip("/")
    img_key_name = "{}/{}.{}".format(key_prefix, img_sha1, img_format)
    upload_args = {}
    if img_format in ["jpg", "jpeg"]:
      upload_args["ContentType"] = "image/jpeg"
    if img_format == "png":
      upload_args["ContentType"] = "image/png"
    if make_public:
      upload_args["ACL"] = "public-read"
    self.bucket.upload_fileobj(
        StringIO(img_bin), img_key_name, ExtraArgs=upload_args)
    return img_key_name

  def generate_obj_url(self, obj_key):
    """Generate url of object.

    Args:
      obj_key: key to object in the bucket.

    Returns:
      the url for object.
    """
    img_url = "{}/{}/{}".format(self.client.meta.endpoint_url,
                                self.bucket_name, obj_key)
    return img_url

  def generate_presigned_url(self, obj_key):
    """Generate a temporary url.

    Args:
      obj_key: key of object in the current bucket.

    Returns:
      presigned url for the target object.
    """
    url = self.client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': self.bucket_name,
                'Key': obj_key})
    return url

  def upload_img_base64(self, img_base64):
    """Save image data to bucket.

    sha1 is used as key for image data.

    Args:
      img_base64: base64 string of image.
    Returns:
      image sha1 hash as key.
    """
    img_sha1 = img_tools.base64_to_sha1(img_base64)
    self.bucket.put_object(Key=img_sha1, Body=img_base64)
    return img_sha1

  def get_object(self, obj_key):
    """Get object binary data from bucket.

    Args:
      obj_key: object key.
    Returns:
      object data.
    """
    res = self.client.get_object(Bucket=self.bucket_name, Key=obj_key)
    obj_data = res["Body"].read()
    return obj_data
