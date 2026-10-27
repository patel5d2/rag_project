# Incident Response Plan: Overview and Roles

## Purpose

This plan describes how the security team detects, contains, and recovers from
cybersecurity incidents. It follows the four-phase lifecycle from NIST SP 800-61:
preparation; detection and analysis; containment, eradication and recovery; and
post-incident activity. Every employee is expected to know how to report an incident,
and every member of the response team is expected to know their role.

## How to report an incident

Any employee who suspects an incident must report it to the Security Operations
Center (SOC) right away. The SOC hotline is staffed 24 hours a day, 7 days a week.
Reports can also be sent to security@example.edu or raised through the "Report
Security Issue" button on the IT portal. Employees should not try to investigate
or "clean up" a suspected compromise themselves, because that can destroy evidence.

## Roles on the response team

- **Incident Commander (IC):** owns the incident from declaration to closure. The IC
  decides the severity level, approves containment actions, and runs status calls.
- **SOC Analyst:** performs triage, gathers logs, and keeps the incident timeline.
- **Forensics Lead:** collects and preserves evidence and maintains chain of custody.
- **Communications Lead:** drafts internal updates and, with Legal, any external notice.
- **Legal and Privacy Officer:** decides whether regulators or affected people must
  be notified and tracks notification deadlines.

The Incident Commander is the only person who can declare an incident closed.

## Phase summary

1. **Preparation.** Maintain contact lists, run tabletop exercises twice a year, and
   keep forensic tools ready on a dedicated jump kit laptop.
2. **Detection and analysis.** Confirm that an alert is a real incident, assign a
   severity level, and open a ticket in the incident tracker.
3. **Containment, eradication and recovery.** Stop the spread, remove the attacker's
   access, and restore systems from known-good backups.
4. **Post-incident activity.** Hold a blameless lessons-learned review within
   10 business days of closure and track every action item to completion.

## Communication rules

During an active incident, use the out-of-band chat channel, not corporate email,
because email may be monitored by the attacker. Status updates go out at the interval
set by the severity level.
