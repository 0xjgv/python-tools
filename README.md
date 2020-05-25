# Installation
You need to have Python3 installed. Tested with Python = 3.7.6
Clone this git repo `git clone git@github.com:juansgaitan/python-tools.git`

Add the path to this repo to your `PATH` by editing your `.bashrc` or `.bash_profile`.

```bash
# ...
export PATH="/path/to/this/repo:$PATH"
# ...
```

# Commands

### SMTP verify emails
`cat emails.txt | smtp_verifier verify`

`smtp_verifier verify EMAIL`

### SMTP get MX records
`cat domains.txt | smtp_verifier mx`

`smtp_verifier mx DOMAIN`

### Entropy
#### Defaults: --number 5
`find ../ -type f -name *.py -not -empty | xargs -n1 cat | entropy`


`find ../ -type f -name * -not -empty | xargs -n1 cat | entropy -n 10`

`entropy someveryveryrandomlongtext`

### Slowloris
#### Defaults: --number 100, --minutes 1, --threads 1
`slowloris IP`

`slowloris IP -n CONNECTIONS -m MINUTES -t THREADS`