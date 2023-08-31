from datetime import datetime
import pandas as pd
import pyodbc
import json
import time
import os

                   
class ParseJson:
    @staticmethod
    def parseJson(data : list = [], config: dict = dict()) -> bool:
                
                """
        Recieve the raw json and parse it
        :parseData: new list to store parse data/items
        :config: to get the configurations or directory paths
        :return data: status of final process [True False]

        """
             
                final_data = list()

                #Old Parser without Node
                try:
                    for i in range(len(data)):
                        try:         
                            try:
                                post_id = data[i].get('post_id')
                            except Exception as e:
                                post_id = -1

                            try:
                                post_url = data[i].get('comet_sections').get('feedback').get('story').get('url')
                            except Exception as e:
                                post_url = -1
                                
                            try:
                                views_count = data[i].get('views_count')
                            except Exception as e:
                                views_count = -1
                            try:
                                comment_count = data[i].get('comet_sections').get('feedback').get('story').get('feedback_context').get('feedback_target_with_context').get('ufi_renderer').get('feedback').get('total_comment_count')
                            except Exception as e:
                                comment_count = -1

                            try:
                                like_count = data[i].get('comet_sections').get('feedback').get('story').get('feedback_context').get('feedback_target_with_context').get('ufi_renderer').get('feedback').get('comet_ufi_summary_and_actions_renderer').get('feedback').get('i18n_reaction_count')
                            except Exception as e:
                                like_count = -1

                            try:
                                share_count = data[i].get('comet_sections').get('feedback').get('story').get('feedback_context').get('feedback_target_with_context').get('ufi_renderer').get('feedback').get('comet_ufi_summary_and_actions_renderer').get('feedback').get('i18n_share_count')
                            except Exception as e:
                                share_count = -1
                            
                            try:
                                basic_info = data[i].get('comet_sections').get('content').get('story').get('comet_sections').get('context_layout').get('story').get('comet_sections').get('actor_photo').get('story').get('actors')
                            except Exception as e:
                                basic_info = -1

                            try:
                                caption = data[i].get('comet_sections').get('content').get('story').get('message').get('text')
                            except Exception as e:
                                caption = -1

                            try:
                                creation_time = data[i].get('comet_sections').get('content').get('story').get('comet_sections').get('context_layout').get('story').get('comet_sections').get('metadata')[0]['story'].get('creation_time')
                            except Exception as e:
                                creation_time = -1

                            try:
                                post_url = data[i].get('comet_sections').get('content').get('story').get('comet_sections').get('context_layout').get('story').get('comet_sections').get('metadata')[0]['story'].get('url')
                            except Exception as e:
                                post_url = -1

                            try:
                                channel_id = basic_info[0]['id']
                            except Exception as e:
                                channel_id = -1

                            try:
                                profile_url = basic_info[0]['profile_url']
                            except Exception as e:
                                profile_url = -1

                            try:
                                page_name = basic_info[0]['name']
                            except Exception as e:
                                page_name = -1

                            try:
                                profile_picture = basic_info[0]['profile_picture'].get('uri')
                            except Exception as e:
                                profile_picture = -1


                            item = {
                                
                                'post_id' : str(post_id)
                                ,'post_url' : str(post_url)
                                ,'comment_count' : str(comment_count)
                                ,'like_count' : str(like_count)
                                ,'share_count' : str(share_count)
                                #,'basic_info' : str(data[i].get('node').get('comet_sections').get('content').get('story').get('comet_sections').get('context_layout').get('story').get('comet_sections').get('actor_photo').get('story').get('actors'))
                                ,'view_count':str(views_count)
                                #,'view_count': -1
                                ,'caption' : str(caption)
                                ,'creation_time' : str(creation_time)
                                ,'post_url' : str(post_url)

                                ,'channel_id'  : str(channel_id)
                                #,'category_type' : str(category_type)
                                ,'profile_url' : str(profile_url)
                                ,'page_name' : str(page_name)
                                ,'profile_picture' : str(profile_picture)
                                
                                
                            }
                            final_data.append(item)
                        except Exception as e:
                            print(e)    
                except Exception as e:
                    print(e)
                
                if len(final_data) > 0:

                    df = pd.DataFrame.from_dict(final_data)

                    df['reporting_date'] = str(datetime.now().date())

                    df['view_count'] = df['view_count'].str.replace('ہزار', 'K')
                    df['view_count'] = df['view_count'].str.replace('لاکھ', 'L')

                    df['like_count'] = df['like_count'].str.replace('ہزار', 'K')
                    df['like_count'] = df['like_count'].str.replace('لاکھ', 'L')

                    df['comment_count'] = df['comment_count'].str.replace('ہزار', 'K')
                    df['comment_count'] = df['comment_count'].str.replace('لاکھ', 'L')

                    df['share_count'] = df['share_count'].str.replace('ہزار', 'K')
                    df['share_count'] = df['share_count'].str.replace('لاکھ', 'L')

                    def convert_to_number(value):
                        try:
                            if 'K' in value:
                                return float(value.replace('K', '')) * 1000
                            elif 'L' in value:
                                return float(value.replace('L', '')) * 100000
                            else:
                                return float(value)
                        except:
                            return value

                    # Apply the function to the 'count' column
                    df['view_count'] = df['view_count'].apply(convert_to_number)
                    df['like_count'] = df['like_count'].apply(convert_to_number)
                    df['comment_count'] = df['comment_count'].apply(convert_to_number)
                    df['share_count'] = df['share_count'].apply(convert_to_number)

                    
                    def GetDate(date):
                        try:
                            return datetime.utcfromtimestamp(int(date)).strftime('%Y-%m-%d')
                        except:
                            return "-1"
                        
                    def GetTime(date):                                                                        
                        try:
                            return datetime.utcfromtimestamp(int(date)).strftime('%H:%M:%S')
                        except:
                            return "-1"    
    
                    
                    df['post_date'] = df['creation_time'].apply(lambda x:GetDate(x))
                    df['post_time'] = df['creation_time'].apply(lambda x:GetTime(x))



                    # Connection details
                    server = 'WIN-U26DHDOFEF0'
                    database = 'dd_stg'  # Change to your database name
                    username = 'ara_1'
                    password = 'Viewlytics@2020'

                    # Create a connection string
                    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

                    # Connect to the SQL Server
                    connection = pyodbc.connect(connection_string)
                    cursor = connection.cursor()
                    try:
                        values_to_delete = [-1, '-1'] 
                        final_df = df[~df['post_id'].isin(values_to_delete)]
                    except Exception as e:
                        final_df = df
                        print(e)
                    # Insert data into the table
                    query = f'''
                            INSERT INTO dd_stg.dbo.fb_daily_post_raw_data (
                                post_id, post_url, comment_count, like_count, share_count, view_count,
                                caption, creation_time, channel_id, profile_url, page_name, profile_picture,
                                reporting_date, post_date, post_time
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                        '''

                    for _, row in final_df.iterrows():
                        values = tuple(row)
                        cursor.execute(query, values)
                        connection.commit()

                    # Close the connection
                    connection.close()