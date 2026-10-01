# EDGE IMPULSE

### Making a project:

- Just Click on Create New Project and name you Project 
- To the left u can see all the tools that we are gonna use in order to make a functioning "AI" 

The administrative part:

|                       | INCBIN                        | xxd                                  |
| --------------------- | ----------------------------- | ------------------------------------ |
| What it does          | Includes binary file directly | Converts binary → C/C++ byte array   |
| Output representation | Binary data                   | C/C++ source code                    |
| Used for              | Embedding files into firmware | Making binary data compiler-friendly |
| ML training?          | ❌                             | ❌                                    |
| Model deployment?     | ✅                             | ✅                                    |

### Data Acquisition:

1. Done either by just uploading it (Soooper simple)
2. Or real time acquisition
   - which requires us to use [Data Forwarder](https://docs.edgeimpulse.com/tools/clis/edge-impulse-cli/data-forwarder)
   - requires [Node.js](https://nodejs.org/en)
   - and Python 
   - and Visual Studio C++
   - and also install EdgeImpulse CLI using ``` npm install -g edge-impulse-cli ```
   - 
