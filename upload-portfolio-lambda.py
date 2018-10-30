import json
import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:083345192164:deployPortfolioTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('kjohnson.io')
        build_bucket = s3.Bucket('build.kjohnson.io')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': 'basestring'})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio deployed successfully!")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The portfolio was not deployed sucessfully!")

    return 'Hello from Lambda'
