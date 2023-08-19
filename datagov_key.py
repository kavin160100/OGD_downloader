# -*- coding: utf-8 -*-
"""Datagov_key.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pIVGSJjriKi8B7xZr8sT23Z3Y5MRJ0sC
"""



import requests
import pandas as pd

class Searcher():
  def search(keyword = ''):
    ''' Searches for datasets in Data.gov.in using the keyword provided.
    Returns a dictionary containing first 10 results of the search and their API links'''

    url = 'https://api.data.gov.in/lists'
    if keyword != '':
      params = {'format': 'json',
                'notfilters[source]': 'visualize.data.gov.in',
                'filters[active]': 1,
                'filters[title]': keyword,
                'filters[source]': 'data.gov.in',
                'sort[created]': 'desc',
                'limit':10,
                'offset': 0}
    else:
      params = {'format': 'json',
                'notfilters[source]': 'visualize.data.gov.in',
                'filters[active]': 1,
                'filters[source]': 'data.gov.in',
                'sort[created]': 'desc',
                'limit':10,
                'offset': 0}

    res= requests.get(url,params=params)
    x = res.json()
    apis = {}
    for item in x['records']:
      apis[item['title']] = item['index_name']
    return apis

  def getdata(apis,format,n):
      '''Access the chosen data using the API key and
      returns the data in the specified format'''

      if len(apis) == 0:
        raise Exception('no resources found')

      title = list(apis.keys())[n]
      link = apis[title]

      dataurl = 'https://api.data.gov.in/resource/' + link
      params = {'api-key': '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b', #Enter the API key
                'format': format}

      resp = requests.get(dataurl,params)
      if format == 'json':
        return resp.json()
      else:
        return resp



if __name__ == "__main__":
  key = input('Enter keyword to search \n')
  form = input('\nEnter data format \n json/csv/xml: ')
  if form not in ['json','csv','xml']:
    print('Incorrect format')
  else:
    try:
      resources = Searcher.search(key)
      i = 0
      for txt in resources.keys():
        print(i,txt)
        i+=1
      num = int(input('\n Enter choice \n'))
      data = Searcher.getdata(resources,form,num)
      if form == 'json':
        df = pd.DataFrame.from_dict(data['records'])
        display(df)
      elif form == 'csv':
        df = pd.DataFrame([x.split(',') for x in (data.text).split('\n')[1:]], columns=[x for x in (data.text).split('\n')[0].split(',')])
        display(df)
      else:
        print(data.text)
    except Exception as err:
      print(err)
  if form == 'json' or form == 'csv':
    option = input('\nDo you want to save the data? Yes/No \n')
    if option.lower() == 'yes':
      df.to_csv('/content/sample_data/test.csv',index = False) #Enter the drive folder link
    else:
      pass

