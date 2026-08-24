# Case: Multi-Object Spatial Pointing Grounding

**Description:** Identifies manipulable items on an industrial table and outputs normalized 2D coordinate points `[y, x]`.  
**Target Model:** `gemini-robotics-er-2`  
**Primary Source:** [Google Developers Blog: Building Physical Agents with Gemini Robotics](https://developers.googleblog.com/en/building-the-next-generation-of-physical-agents-with-gemini-robotics-er-15/)

### Prompt
```text
Point to no more than 10 items in the image.
Return JSON format: [{"point": [y, x], "label": "<name>"}]
with coordinates normalized between 0-1000.
```

### Sample Output (JSON)
```json
[
  {"point": [520, 310], "label": "socket_wrench"},
  {"point": [710, 640], "label": "multimeter"}
]
```
