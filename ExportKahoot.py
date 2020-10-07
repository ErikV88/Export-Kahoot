import requests
import os
import ssl   
import json
import csv

class Questions:
    questions=[]
    def add(self,question):
        self.questions.append(question)

    def toExel(self,filename):
        rows=[]
        for q in self.questions:
            row=[]
            row.append(q.question)
            rows.append(row)
           

            for a in q.alternatives:
                rows.append(a)
            rows.append([])

            with open(filename, 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(rows)


class Question:
    def __init__(self,question,alternatives):
        self.question=question
        self.alternatives=alternatives


class ExportKahoot:
    api_auth=' https://create.kahoot.it/rest/authenticate'
    api_url='https://create.kahoot.it/rest/kahoots/%s/card/?includeKahoot=true'
    cookies=None
    csv_filename=''

    def __init__(self):
        self.username=input('Kahoot User Name:')
        self.password=input('Kahoot Password:')

        self.auth()

    def auth(self):
        session = requests.Session()
        myobj={"username":self.username,"password":self.password,"grant_type":"password"}
        response = session.post(self.api_auth, data = myobj)
        self.cookies=session.cookies.get_dict()

    def export(self):
        id=input('What ID?:')
        headers = {'content-type': 'application/json'}
        kahoot=json.loads(requests.get(self.api_url%(id),headers=headers,cookies=self.cookies).text.encode("utf-8"))['kahoot']        
        questions=kahoot['questions']
        filename='%s.csv'%(str(kahoot['title']).replace(' ',''))

        questions_out=Questions()
        for q in questions:
            question_string=''
            choices=[]
            choices_obj=[]

            try:
                question_string=q['question']
                try:
                    choices=q['choices']

                    for c in choices:
                        r=[]
                        r.append(c['answer'])
                        r.append(c['correct'])
                        choices_obj.append(r)
                except:
                    choices=[]

            except:
                question_string=''
               
                try:
                    choices=q['choices']

                    for c in choices:
                        r=[]
                        r.append(c['answer'])
                        r.append(c['correct'])
                        choices_obj.append(r)
                except:
                    choices=[]


               
            question=Question(question_string,choices_obj)
            questions_out.add(question)


        questions_out.toExel(filename)

        print('Kahoot is exported to same folder: ' + os.getcwd())

        self.export()

Export=ExportKahoot()

Export.export()



