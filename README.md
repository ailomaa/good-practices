# README

If you want to try running code in this repo, do the following:

- clone this repo
- cd into the repo
- create a python venv and activate it
- install python requirements
- check contents of `run.sh`
- then run `run.sh`

Like this:
```console
git clone git@github.com:ailomaa/good-practices.git
cd good-practices
python -m venv good-venv
source good-venv/bin/activate
which python         # making sure we activated the venv
pip install -r requirements.txt
cat run.sh
./run.sh
```

Once you are done, you can remove the repository together with the venv.
```console
deactivate     # deactivate the venv
cd ..
rm -rf good-practices/
```

Docs are located in `docs/`

## License

Code (`wordfreq.py`, `run.sh`) is MIT licensed — see [LICENSE](LICENSE).
Documentation and sample data are CC BY 4.0 — see [LICENSE-docs](LICENSE-docs).
Reuse and adapt either freely, with credit.
