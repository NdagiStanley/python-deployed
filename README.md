# python-deployed

Exploring different ways to deploy a Python application.

> _Anything with an * (asterisk) is explained at the very end._
>
> *Shout out!* **Andrew T Baker** gave [this talk on PyCon 2017](https://youtu.be/vGphzPLemZE) from which a number of the options and mostly the Pros and Cons tables come from.

New to Python? Start [here](https://www.python.org/about/gettingstarted).

More?

- [Awesome Python](https://awesome-python.com/) list
- Feel free to check out my [All things Python](https://gist.github.com/NdagiStanley/bf9db623e8a96ef2ab631a28c9a1eba8) gist

## Run server

### Virtual environment

```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 hello.py
```

Or use these alternatives*.

Server running at [localhost:5000](http://localhost:5000)

## Deployment options

1. ngrok

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | Fast and easy | Runs locally hence will stop when you close your machine  |
    | Handy for demos                   | Random domains                        |
    | Allows you to hack on webhooks    | Doesn't scale                         |

    > Steps

    1. Install [ngrok](https://ngrok.com/download)
    1. [Run server](#Run-server), then...

    ```bash
    ngrok http 5000
    ```

    **Note**: _Request inspector lives in [localhost:4040](http://localhost:4040) when `ngrok` is running._

1. Heroku

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | 24/7 for free             | Scaling is easy but pricey                        |
    | Zero server management    | Some add-ons are better than others               |
    | Add-ons ecosystem         | limited server customization                      |

    > Steps

    - Install [gunicorn](https://gunicorn.org/)

      alternative: [uvicorn](https://www.uvicorn.org/) (ASGI server)

        ```bash
        pip install gunicorn
        ```

    - `Procfile`

        ```txt
        web: gunicorn hello:app --log-file -
        ```

    - Deploy app on [Heroku](https://herokuapp.com/)
        1. Heroku [CLI](https://devcenter.heroku.com/articles/heroku-cli)
        1. `heroku create`. You'll be prompted to log in, if you're doing this for the first time.
        1. `git push heroku master`
        1. `heroku open`

    **Note**: _In Heroku, the bundling happens on Heroku's servers. Compare Zappa (below)_

1. AWS Lambda

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | Economical for small to medium loads | Relatively new technique |
    | Good for 'spiky' traffic | Less fun w/o zappa |
    | Zero server config | Can be tricky to troubleshoot |

    > Steps (Zappa)

    - `pip install zappa`
    - `zappa init`

        - [x] Install AWS CLI (MacOS: `brew install awscli`, Others: [AWS CLI version 2 user guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html))

        Options:

        - environment: `production`
        - private s3 bucket: (default 'zappa-<RANDOM_STRING>')
        - app's function: (default 'hello.app')
        - deploy globally?: (default 'n')

    - `zappa deploy production`

    **Note**: _For zappa the app is bundled locally before it's pushed to AWS. Compare Heroku (above)_

1. Virtual Machines

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | Full control          | More work for you |
    | Scales as much as your wallet     | There's more to learn |
    | Economical.. if you're careful    | Harder to predict ultimate costs  |

    Most companies deploy on VMs in the cloud.

    Most cloud providers offer VMs; Amazon: **EC2**, Google: **Google Compute Engine**

    > Steps (Compute Engine)

    - Create a project on GCP
    - Select VM Machines (**Menu/Compute Engine/VM machines**)
    - Enable **Compute Engine API**
    - Create Instance (Options: `Name`, `Region`, `Machine type`: _Ubuntu (my preference)_, `Firewall`: _Allow HTTP traffic_)
    - After creation, Click **View gcloud command** (on the Dropdown on **SSH** column of the instance)
    - Click **RUN IN CLOUD SHELL** OR copy, paste, and run in your local shell

        - `gcloud init`

        [**gcloud** CLI cheatsheet](https://cloud.google.com/sdk/docs/cheatsheet)
    - In the shell, run: (_Ubuntu 16_)

        ```bash
        cd /var
        sudo su
        apt update
        apt install python3-pip -y
        pip install --upgrade pip
        git clone https://github.com/NdagiStanley/python-deployed.git
        cd python-deployed
        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
        gunicorn hello:app --log-file - --bind 0.0.0.0:80 # -b :80
        ```

1. Digital Ocean

    The manual approach (w/o Docker [_see below **#6**_]), configuring the server environment directly.

    > Steps

    - Create Droplet
    - SSH into Droplet
    - In the shell, run: (_Ubuntu 20_)

        ```bash
        cd /var
        sudo su
        apt update
        apt install python3-pip python3-venv -y
        pip3 install --upgrade pip
        git clone https://github.com/NdagiStanley/python-deployed.git
        cd python-deployed
        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
        gunicorn hello:app --log-file - --bind 0.0.0.0:80 # -b :80
        ```

1. Docker

    | Pros                  | Cons                  |
    | ---                   | ---                   |
    | Helps with dev/ prod parity   | Works best when you go all-in |
    | Nice for microservices | Has its own learning curve |

    (Show then Tell)

    - Create `Dockerfile`
    - `docker build -t stanmd/python-deployed .`
    - `docker push stanmd/python-deployed`
    - `docker run -p 5000:5000 stanmd/python-deployed`
    - Install `docker-machine` and create a host

        Provisioning hosts on cloud providers: [Digital Ocean](https://docs.docker.com/machine/examples/ocean/) (DO), [AWS EC2](https://docs.docker.com/machine/examples/aws/)

        For example: (Creating a Droplet)

        ```bash
        # docker-machine create --driver digitalocean --digitalocean-access-token xxxxx [droplet-name]
        docker-machine create --driver digitalocean --digitalocean-access-token xxxxx python-deployed
        ```

        Don't mind the error that reads: _`Error creating machine: Error running provisioning: Unable to verify the Docker daemon is listening: Maximum number of retries (10) exceeded`_.  The droplet was created but has some issues. I ran `docker-machine regenerate-certs [droplet-name]` and I proceeded successfully.

    - Run `docker-machine ls` to confirm the active host. The active host has an asterisk on the ACTIVE column.

    - If you need to change the active host/machine, run `docker-machine env python-deployed`, followed by `eval $(docker-machine env python-deployed)`. This specifies that the docker commands run thereafter run on that host/machine.
    - `docker pull stanmd/python-deployed`
    - `docker run -p 5000:5000 stanmd/python-deployed`
    - `docker-machine ip python-deployed` prints out the **<DROPLET_IP>**
    - Go to **<DROPLET_IP>:5000** on your browser

    To share the credentials for `docker-machine` (with a team mate, for example) use [machine-share](https://github.com/bhurlow/machine-share) (installable via `npm install -g machine-share`) but this only works if you created the machine using `docker-machine` in the first place.

---

### Reference

- **alternatives*** - _[My python virtual environment notes](https://gist.github.com/NdagiStanley/bf9db623e8a96ef2ab631a28c9a1eba8#file-virtual_envs-md)_
