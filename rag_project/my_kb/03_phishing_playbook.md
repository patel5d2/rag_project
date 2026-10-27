# Playbook: Phishing Email

## Trigger

This playbook starts when a user reports a suspicious email with the "Report Phish"
button, or when the mail gateway flags a message that has already been delivered.

## Triage

1. Pull the original message with full headers from the reported-phish mailbox.
2. Check the Return-Path, the Received chain, and the SPF, DKIM and DMARC results.
   A DMARC failure combined with a look-alike sender domain is a strong phishing signal.
3. Extract every URL and attachment. Detonate attachments in the malware sandbox,
   never on an analyst workstation.
4. Search the mail logs for the same sender, subject, or URL to find every recipient.

## Containment

- Purge all copies of the message from every mailbox with the mail admin console.
- Block the sender domain and the URLs at the mail gateway and the web proxy.
- If any user clicked the link, check the proxy logs to confirm whether the page loaded.

## If credentials were entered

Treat any user who typed a password into the phishing page as a compromised account.
The response is SEV2 at minimum.

1. Reset the user's password and revoke all active sessions and refresh tokens.
2. Re-register the user's MFA device in person or over a verified video call.
3. Review sign-in logs for the last 14 days for logins from new countries or devices.
4. Check the mailbox for new forwarding rules, which attackers add to keep access.

## If an attachment was opened

Isolate the endpoint from the network with the EDR console, then hand it to the
forensics lead. Do not power the machine off, because memory evidence would be lost.

## Closure

Send the reporting user a thank-you note, because positive feedback raises reporting
rates. Add the indicators of compromise to the threat intelligence platform. A
phishing incident can be closed once all copies are purged and every affected account
has been reset and reviewed.
