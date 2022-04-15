AWS_ACCESS_KEY_ID = 'AKIAS4ICQJ4MG7G4N4UU'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'delivery-azikdev-files'
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
        'PASSWORD': 'angorelegan2002',
        'HOST': 'database-1.cmumimcezu99.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

SECRET_KEY = 'django-secure-+=bqmnb*ixv9)49bk7txyr4-1onc=^=e)msl3$qus_lhvyt#cn'
