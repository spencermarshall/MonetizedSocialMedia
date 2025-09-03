import boto3
import random
import datetime
import json

ARNS = [
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/JediMemes",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/Marvel_Meme",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/BB_meme",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/SW_Question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/MiddleEarthMeme",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTR_art",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/BB_text_quote_6pm",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/HarryPotter_redditmeme_post",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTR_question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/Marvel_redditmeme_post",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTRMeme-Solo-Account",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/AcrossTheGalaxy",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/HP_meme",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/BB_question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/HarryPotter_Question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/HobbitMemes",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTR_quote",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/SW_art",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/Daily_6pm",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTR_meme",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/TolkienMemes_Question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/LOTR_redditmeme_post",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/Marvel_Question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/TolkienMemes",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/MiddleEarth_Question",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/BreakingBad_redditmeme_post",
    "arn:aws:scheduler:us-east-1:975050204241:schedule/default/AcrossTheGalaxy_Question"
]

# Add your ARNs here as a list of strings, e.g., ['arn:aws:scheduler:us-east-1:123456789012:schedule/default/schedule1', 'arn:aws:scheduler:us-east-1:123456789012:schedule/default/schedule2']

client = boto3.client('scheduler')
def UpdateMinute(event, context):
    current_hour = datetime.datetime.utcnow().hour
    updated_count = 0
    for arn in ARNS:
        parts = arn.split('/')
        if len(parts) < 2:
            print(f"Invalid ARN format: {arn}")
            continue
        group = parts[-2]
        name = parts[-1]
        try:
            # Get the full schedule configuration
            resp = client.get_schedule(GroupName=group, Name=name)
            expr = resp['ScheduleExpression']
            if not expr.startswith('cron(') or not expr.endswith(')'):
                print(f"Unsupported schedule expression format for {arn}: {expr}")
                continue
            fields = expr[5:-1].split()
            if len(fields) != 6:
                print(f"Unexpected cron fields count for {arn}: {expr}")
                continue
            hours = fields[1]
            try:
                hours_list = [int(h) for h in hours.split(',')]
            except ValueError:
                print(f"Failed to parse hours as comma-separated integers for {arn}: {hours}")
                continue
            if current_hour in hours_list:
                new_min = str(random.randint(18, 42))
                new_expr = f"cron({new_min} {hours} {' '.join(fields[2:])})"
                # Preserve required fields from the existing schedule
                client.update_schedule(
                    GroupName=group,
                    Name=name,
                    ScheduleExpression=new_expr,
                    FlexibleTimeWindow=resp['FlexibleTimeWindow'],
                    Target=resp['Target'],
                    # Include other optional fields if they exist in the original schedule
                    State=resp.get('State', 'ENABLED'),
                    Description=resp.get('Description', ''),
                    ScheduleExpressionTimezone=resp.get('ScheduleExpressionTimezone', None)
                )
                print(f"Updated schedule for {arn} with minute {new_min} (new expression: {new_expr})")
                updated_count += 1
        except Exception as e:
            print(f"Error processing {arn}: {str(e)}")
    print(f"Updated {updated_count} schedules this run")
    return {
        'statusCode': 200,
        'body': f"Updated {updated_count} schedules"
    }