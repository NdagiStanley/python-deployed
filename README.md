# python-deployed
Exploring different ways to deploy a Python application

## Run server

### Virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 hello.py
```

Server running at [localhost:5000](http://localhost:5000)

## Deployment options

1. ngrok

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | Fast and easy | Runs locally hence will stop when you close your machine  |
    | Handy for demos                   | Random domains                        |
    | Allows you to hack on webhooks    | Doesn't scale                         |

    ### Steps
    1. Install [ngrok](https://ngrok.com/download)
    1. [Run server](#Run-server), then...

    ```
    ngrok http 5000
    ```

    **Note**: _Request inspector lives in [localhost:4040](http://localhost:4040) when `ngrok` is running._

1. Heroku

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | 24/7 for free             | Scaling is easy but pricey                        |
    | Zero server management    | Some add-ons are better than others               |
    | Add-ons ecosystem         | limited server customization                      |

    ### Steps

    - Install `gunicorn`
        ```
        pip install qunicorn
        ```

    - `Procfile`

        ```
        web: gunicorn hello:app --log-file -
        ```

    - Deploy app on [Heroku](https://herokuapp.com/)
        1. Heroku [CLI](https://devcenter.heroku.com/articles/heroku-cli)
        1. `heroku create`. You'll be prompted to log in, if you're doing this for the first time.
        1. `git push heroku master`
        1. `heroku open`

1. AWS Lamda

    Zappa

    - `pip install zappa`
    - `zappa init`
    - `zappa deploy production`
