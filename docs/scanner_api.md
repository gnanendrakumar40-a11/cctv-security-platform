\# Scanner Output Contract



\## Purpose



The scanner produces a structured JSON report that can be consumed by

the backend, database, frontend, and machine-learning components.



\## Result Structure



```json

{

&#x20;   "target": "127.0.0.1",

&#x20;   "device": "Possible DVR, NVR, or web service",

&#x20;   "ports": \[],

&#x20;   "findings": \[],

&#x20;   "risk\_score": 0,

&#x20;   "risk\_level": "INFO"

}

