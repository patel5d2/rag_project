# Incident Severity Levels and Escalation

The Incident Commander assigns a severity level during detection and analysis. The
level sets how fast the team must respond, who is paged, and how often updates go out.
The level can be raised or lowered as new facts appear.

## SEV1: Critical

A SEV1 incident is an active compromise of a critical system, confirmed data
exfiltration, or ransomware spreading across the network.

- Acknowledge within 15 minutes, at any hour.
- Page the Incident Commander, the CISO, and the on-call forensics lead.
- Status updates to leadership every 60 minutes.
- Legal is engaged immediately.

## SEV2: High

A SEV2 incident is a confirmed compromise of a single host or account with no evidence
yet of spread or data loss, such as a successful phishing login.

- Acknowledge within 1 hour.
- Page the Incident Commander and the on-call SOC analyst.
- Status updates every 4 hours.

## SEV3: Medium

A SEV3 incident is suspicious activity that is contained or low impact, such as malware
blocked by endpoint protection after it ran briefly.

- Acknowledge within 4 business hours.
- Handled by the SOC queue; no page required.
- Daily status update in the incident ticket.

## SEV4: Low

A SEV4 incident is a policy violation or reconnaissance with no compromise, such as a
port scan from the internet against the perimeter firewall.

- Acknowledge within 2 business days.
- Logged and reviewed in the weekly security meeting.

## Escalation rules

If the assigned owner has not acknowledged a SEV1 or SEV2 page within the target time,
the page escalates automatically to the next person on the on-call rotation, and then
to the CISO. Any responder may raise the severity level; only the Incident Commander
may lower it. If an incident involves personal data, it is treated as at least SEV2
until Legal confirms otherwise.
