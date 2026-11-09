# Sources

All 12 alerts in `my_alerts.json` and the 8 practice alerts in the notebook are written by me, in my own
words. None is copied from an employer or production console. Hostnames, users, tickets and the organisation
("acme") are invented. IP addresses come from the reserved documentation ranges (RFC 5737:
192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) and private ranges, so none points at a real system.

I used the references below to make each alert *type* realistic: which event IDs exist, what fields a
detection carries, and which behaviour an analyst treats as malicious.

| Alert | Type it is based on | Reference |
|---|---|---|
| E1 | EDR ransomware behaviour, shadow copy deletion | MITRE ATT&CK T1490 Inhibit System Recovery, https://attack.mitre.org/techniques/T1490/ |
| E2, C3 | Windows failed/successful logon events 4625 / 4624 | Microsoft Learn, "4625(F): An account failed to log on" and "4624(S): An account was successfully logged on"; ATT&CK T1110 Brute Force, https://attack.mitre.org/techniques/T1110/ |
| E3 | EDR credential dumping from LSASS | ATT&CK T1003.001 OS Credential Dumping: LSASS Memory, https://attack.mitre.org/techniques/T1003/001/ |
| E4, C5 | AWS CloudTrail ConsoleLogin, CreateAccessKey, PutBucketPolicy | AWS CloudTrail User Guide, "AWS Management Console sign-in events"; AWS IAM User Guide, root user best practices; ATT&CK T1078.004 Valid Accounts: Cloud Accounts |
| E5 | EDR process lineage, Office spawning mshta | ATT&CK T1218.005 System Binary Proxy Execution: Mshta, https://attack.mitre.org/techniques/T1218/005/ |
| E6 | IDS DNS tunnelling / high-volume TXT queries | ATT&CK T1071.004 Application Layer Protocol: DNS, https://attack.mitre.org/techniques/T1071/004/ |
| C1 | Antivirus detection of the EICAR test file | EICAR, "Anti-Malware Testfile", https://www.eicar.org/download-anti-malware-testfile/ |
| C2 | Suricata / Emerging Threats Log4j signature from a scanner | NVD CVE-2021-44228, https://nvd.nist.gov/vuln/detail/CVE-2021-44228; Emerging Threats open ruleset naming (ET EXPLOIT, ET INFO) |
| C4 | PowerShell script block logging, event 4104 | Microsoft Learn, "about_Logging_Windows" (PowerShell script block logging) |
| C6 | PsExec used by a patching service account | Microsoft Sysinternals, "PsExec"; ATT&CK S0029 PsExec, https://attack.mitre.org/software/S0029/ |

Framework: LangGraph documentation (StateGraph, conditional edges, `MemorySaver` checkpointer, thread ids),
https://langchain-ai.github.io/langgraph/, and LangChain Core runnables for the chain comparison.
