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

### Entropy
`find ../ -type f -name *.py -not -empty | xargs -n1 cat | entropy`

`entropy someveryveryrandomlongtext`

### SMTP verifier
`cat emails.txt | smtp_verifier verify`

`smtp_verifier verify EMAIL`
