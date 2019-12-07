import requests, json, os, psycopg2

def extract_all_jobs_href(response):
    result = []
    for i in response.xpath("//a[@target='_blank'][@data-controller='utm-tracking'][contains(@href, '/it-jobs/')]"):
        job_link = i.xpath("./@href").get()
        job_details = job_link.split("/")[2]
        result.append(job_details)

    return result

def slack_data_modified(data):
    output = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{job_title}* - *{company_name}* - <{link}|link>\n```{job_details}```".format(
                        job_title=data['job_title'],
                        company_name=data['company_name'],
                        job_details=data['job_details'],
                        link=data['link'])
                }
            }
        ]
    }
    return output


def insert_data(href_value):
    try:
        connection = psycopg2.connect(
            user="it",
            password="password",
            host="127.0.0.1",
            port="5432",
            database="it_viec")
        cursor = connection.cursor()

        """
            Check whether data exists before insert 
        """

        cursor.execute(
            """select exists (select true from job where href=%s)""",
            href_value
        )
        data_existed = cursor.fetchone()[0]
        if data_existed == True:
            return "existed, ignored"
        
        elif data_existed == False:
            cursor.execute(
                """INSERT INTO job (href) VALUES(%s);""", 
                href_value
            )
            connection.commit()
            print("""{href} not found, \ninserted {href} into the database\n""".format(href=href_value))
            return "not existed, imported"

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print(error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()