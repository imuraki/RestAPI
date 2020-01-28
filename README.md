# RestAPI
Contains REST API's developed for a loan application

This Project uses Django REST Framework to develop RESTful API's for a loan application.

Here I can:
1.POST an application with an AppID and username(each user can try to submit mutliple applications)
2.GET a loan application
3.GET the status of a loan application given a loanapp id
4.DELETE an loan application

The local host supports the following HTTP method calls

1. The loan applications can be GET through GET /loanapp/ -> http://127.0.0.1:8000/loanapp/ -> Which lists all the loanapplication data
2. GET /loanapp/1 -> http://127.0.0.1:8000/loanapp/1 -> Which lists loan application data of AppID = 1
3. The loan application can be POST through POST /loanapp/ loanapplication data -> http://127.0.0.1:8000/loanapp/ -> which consumes the json and returns the link to that respective application data
3. GET /status/ -> http://127.0.0.1:8000/status/ -> Which lists the sttaus of all submitted applications
4. http://127.0.0.1:8000/status/?loanappid=1 -> Which gets the status of the loanapplication with AppID = 1
5. DELETE /loanapp/1 -> which deletes the loan application with AppID = 1
6. When a new application with almost same information is updated , only the respective field changes are updated but not overwritten. Here I assumed username is unique for each user

