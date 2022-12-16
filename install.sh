# Install smtp_verifier to current shell
# idea: ln -sf ./.venv/bin/smtp_verifier /usr/bin/smtp_verifier

smtp_path=./.venv/bin/smtp_verifier
if [ -f "$smtp_path" ]; then
	ln -sf "$smtp_path" /usr/local/bin/smtp_verifier
	echo "smtp_verifier installed"
fi
