# Playbook: Ransomware

## Trigger

This playbook starts when endpoint protection reports mass file encryption, when users
find ransom notes, or when file shares suddenly fill with files that have an unknown
extension. Ransomware is always declared SEV1.

## First 30 minutes

1. Isolate affected hosts with the EDR console. If EDR is unavailable, unplug the
   network cable, but leave the machine powered on.
2. Disable the compromised accounts, especially any domain administrator accounts
   seen in the alerts.
3. Take the backup servers offline from the production network so the attacker
   cannot encrypt or delete them.
4. Open the out-of-band chat channel and page the Incident Commander.

## Scoping

- Identify patient zero: the first host that showed encryption or the first malicious
  login. Most ransomware here arrives through phishing or an exposed remote desktop.
- Check for data exfiltration before encryption, by reviewing firewall egress logs for
  large uploads to unfamiliar cloud storage. Double-extortion groups steal data first.
- Photograph the ransom note and record the group name and any contact address.

## Eradication and recovery

Do not restore any system until the initial access path has been found and closed;
otherwise the attacker simply encrypts it again. Rebuild infected hosts from a clean
gold image rather than trying to remove the malware. Restore data from backups only
after the backups have been scanned and verified as clean. Our backup policy keeps an
immutable copy for 30 days, so the restore point must be from before the first sign
of attacker activity.

## Ransom payment

The organization's policy is not to pay ransoms. Any discussion of payment must
involve executive leadership, Legal, and law enforcement. The decision is never made
by the response team alone. Report the attack to the FBI through IC3.

## After recovery

Reset every privileged credential in the domain, including service accounts, and
reset the KRBTGT account password twice. Watch the restored systems closely for at
least 30 days.
