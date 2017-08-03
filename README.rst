Usage:

$ WEBHOOK_SCRIPT=$PWD/test_script.py python simple_webhook.py


$ curl -H "Content-Type: application/json" -X POST -d '{"data":"xyz"}' http://localhost:8000/
