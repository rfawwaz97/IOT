def get_data_from_dynamodb():
    try:
            import boto3
            from boto3.dynamodb.conditions import Key, Attr

            dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
            table = dynamodb.Table('2M1C-Fawwaz-GuardRoom')

            startdate = '2019-02-17T'
            response = table.query(
                KeyConditionExpression=Key('deviceid').eq('deviceid_shakir') & Key('datetimeid').begins_with(startdate),
                ScanIndexForward=False
            )

            items = response['Items']

            n=10 # limit to last 10 items
            data = items[:n]
            data_reversed = data[::-1]
            return data_reversed
    except:
        import sys
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


if __name__ == "__main__":
    query_data_from_dynamodb()

