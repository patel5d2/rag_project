# Evidence Handling and Chain of Custody

## Why it matters

Evidence collected during an incident may be needed for a criminal case, an insurance
claim, or a regulator. If its handling cannot be documented, it may be rejected. The
Forensics Lead is responsible for every item of evidence from collection to disposal.

## Order of volatility

Collect the most volatile evidence first, because it disappears soonest:

1. CPU registers and cache, then memory (RAM).
2. Network state: active connections, routing tables, and the ARP cache.
3. Running processes and logged-in users.
4. Disk contents.
5. Remote logs and archived backups.

Capture memory before disk imaging, and never shut down a running machine to collect it.

## Disk imaging

Always work on a copy, never on the original drive. Use a hardware write blocker when
imaging a physical disk. Calculate a SHA-256 hash of the original and of the image;
the two hashes must match before analysis begins. Record both hashes on the chain of
custody form.

## Chain of custody form

Every evidence item gets its own form, which records:

- a unique evidence ID and a description of the item;
- who collected it, when, and where;
- every transfer: who handed it over, who received it, the date and time, and why;
- where it is stored.

Physical evidence goes into a sealed, labeled evidence bag and is kept in the locked
evidence safe in the SOC. Only the Forensics Lead and the CISO have the safe code.

## Log retention

Security logs are kept for one year online and an additional six years in archive.
When an incident is declared, a legal hold is placed on all related logs and mailboxes,
which suspends normal deletion until Legal releases the hold.

## Disposal

Evidence is kept until Legal confirms that no case, claim, or audit still needs it.
Digital copies are then securely wiped, and the disposal is recorded on the form.
