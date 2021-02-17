##!/usr/bin/python3
# b4r_dpo.py
# this is just a demo file to make sure we can pull data from b4r
# 2021.2.17, vince paris
# from dpo import  Dpo
# import  sys, os, argparse
# import  pytest
# aeoPython = os.environ["EBSAF_ROOT"] + "/aeo/python"
# sys.path.append(aeoPython)
#
# import simbaUtils
#
# simbaUtils.readConfig()
# tmp = "/models/analysis/cimmyt/phenotypic/asreml"
# parser = argparse.ArgumentParser()
# parser.add_argument("input", type=str, help="Input folder")
# args = parser.parse_args()
# request = os.environ["EBSAF_ROOT"] + tmp + "/templates/" \
#           + sys.argv[1] + "/" + sys.argv[1] + ".req"


import json
import requests

endpoint = "https://b4rapi-uat.ebsproject.org/v3/crops"
headers = {"Authorization": "Bearer eyJ4NXQiOiJaalJtWVRNd05USmpPV1U1TW1Jek1qZ3pOREkzWTJJeU1tSXlZMkV6TWpkaFpqVmlNamMwWmciLCJraWQiOiJaalJtWVRNd05USmpPV1U1TW1Jek1qZ3pOREkzWTJJeU1tSXlZMkV6TWpkaFpqVmlNamMwWmdfUlMyNTYiLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoibVJRSk95cjBGN1hWY0xlQkxaNnlMZyIsImh0dHA6XC9cL3dzbzIub3JnXC9jbGFpbXNcL3VzZXJuYW1lIjoiMTA4OTQyNzQyODI2NzExNDc0MjQ0Iiwic3ViIjoidmcyNDlAY29ybmVsbC5lZHUiLCJodHRwOlwvXC93c28yLm9yZ1wvY2xhaW1zXC9waG90b3VybCI6Imh0dHBzOlwvXC9saDQuZ29vZ2xldXNlcmNvbnRlbnQuY29tXC8tSG1tSkJMRmRjZkFcL0FBQUFBQUFBQUFJXC9BQUFBQUFBQUFBQVwvQU1adXVjbF9yWTdQRFBJTnpZZ0NhMjZ2MVl6R3VIellkZ1wvczk2LWNcL3Bob3RvLmpwZyIsImFtciI6WyJTQU1MU1NPQXV0aGVudGljYXRvciJdLCJpc3MiOiJodHRwczpcL1wvZWJzLmNpbW15dC5vcmc6OTQ0M1wvb2F1dGgyXC90b2tlbiIsImh0dHA6XC9cL3dzbzIub3JnXC9jbGFpbXNcL2dpdmVubmFtZSI6IlZpc2hudSIsImh0dHA6XC9cL3dzbzIub3JnXC9jbGFpbXNcL2lkZW50aXR5XC9lbWFpbFZlcmlmaWVkIjoidHJ1ZSIsImF1ZCI6IjJFbGtRZUpLME5YNldINnR2UDY5WGEwWE16QWEiLCJjX2hhc2giOiJvMkdiLXh2MFZRdG5Pd001TWJnamxRIiwibmJmIjoxNjEzNjAxMDIyLCJodHRwOlwvXC93c28yLm9yZ1wvY2xhaW1zXC9sb2NhbCI6ImVuIiwiaHR0cDpcL1wvd3NvMi5vcmdcL2NsYWltc1wvZnVsbG5hbWUiOiJWaXNobnUgR292aW5kYXJhaiIsImF6cCI6IjJFbGtRZUpLME5YNldINnR2UDY5WGEwWE16QWEiLCJodHRwOlwvXC93c28yLm9yZ1wvY2xhaW1zXC9lbWFpbGFkZHJlc3MiOiJ2ZzI0OUBjb3JuZWxsLmVkdSIsImh0dHA6XC9cL3dzbzIub3JnXC9jbGFpbXNcL2xhc3RuYW1lIjoiR292aW5kYXJhaiIsImV4cCI6MTYxMzYwNDYyMiwiaWF0IjoxNjEzNjAxMDIyfQ.FxTt9Hk-y-6YmUYuN2Nw6BO1NTJ09KrCzTlGqEqH6fZuSH6QTk0Hvc0AmnKVeBKRDOLIUZTynxJb-Yn_wG6n6xHL3yhg9ay0QuYZMXb-3wsgToezPGeX_pysTp2jOVhRIt6TeQnxQu17ko7xCfr6D_9-g9XpmTjXcNMhD8UPAN3ct9fCDE0EkWLwHpSrZZtSQdIumTpRvn-HIPFHXKeZ1vMQD5n0yynp5vFVInrrYiEof-dkwTdU3wBnWvocmUf5fuDKnQAi6oYzzq6579WoRuZqxk8Lyw5eiMW9xGIc4kOdrR1_t4LXGWDu8AUiZAEpNQSjTRJHyUg5xjbBjiRFQw"}

json = requests.get(endpoint, headers=headers).json()

print(json['result']['data'][0]['cropCode'])

print(json['result']['data'][0])

# df = pd.read_json(x)
# print(df)
