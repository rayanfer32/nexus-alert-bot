### Whale notifier bot for Nexus Blockchain

### TODO:




### Installation

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Usage

```sh
python3 main.py
```

OR if you want to run it as a service:

```sh
source venv/bin/activate
pm2 start "python3 main.py" --name whalebot
```

### Windows
```cmd
venv\Scripts\activate
python main.py
```

### Features
- [x] Send errors to multiple Maintainer chat ids
- [x] Report maintainers when base url goes down
- [x] Configure NXS_BASE_URL from .env

### Improvements Todo
> Yet to be discovered. 