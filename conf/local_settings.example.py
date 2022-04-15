AWS_ACCESS_KEY_ID = 'AAAAaaaBBBBccccDDD'
AWS_SECRET_ACCESS_KEY = 'AAAAaaaBBBBccccDDDAAAAaaaBBBBccccDDD'
AWS_STORAGE_BUCKET_NAME = 'example-bucket-name'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_ADDRESSING_STYLE = "virtual"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Delivery',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = 'django-secure-+=bqmnb*ixv9)49bk7txyr4-1onc=^=e)msl3$qus_lhvyt#cn'

TWILIO_ACCOUNT_SID = "AAAAaaaBBBBccccDDD"
TWILIO_AUTH_TOKEN = "AAAAaaaBBBBccccDDDAAAAaaaBBBBccccDDD"
TWILIO_FROM_NUMBER = "+12182923493"

TWILIO_SEND_SMS = False
