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
   - Python needed 
   - Arduino needed
   - Have all the proper audio in one folder (30 actual)
   - Have all the background in one folder (20 bg)
   - So upload one folder at a time and label it accordingly
   - It is important to have 1 and 3 whistles in the background part or else the AI may false trigger after just one whistle, just cause it is in the bg we don't remove it from the actual trigger but teaches when to trigger
   - Splits it 80/20 to Train/Test 

2. Or real time acquisition
   - which requires us to use [Data Forwarder](https://docs.edgeimpulse.com/tools/clis/edge-impulse-cli/data-forwarder)
   - requires [Node.js](https://nodejs.org/en)
   - and Python 
   - and Visual Studio C++
   - and also install EdgeImpulse CLI using ``` npm install -g edge-impulse-cli ```


### Impulse Creation:

1.Target Device ->  Espressif ESP-EYE (ESP32 240MHz)

2.It does exactly as the window says: 
   - An impulse takes raw data, uses signal processing to extract features, and then uses a learning block to classify new data
   - Window size should approx to how much the keyword should be 
   - and stride decides the next part after shifting the data by that amount of time
   - decreasing stride is better but it also makes it slower due to many overlapping part

3.Processing Block - MFE
   - MFCC is commonly used for speech and keyword recognition, while MFE is a simpler time–frequency energy representation that can work well for general audio classification

4.Learning Block - Classifier (Regression if want to check say what frequency the whistle is..)

### Pipe line is done :

``` Microphone → Raw audio → MFE → Features → Classifier → double_whistle / background ```

## The Training Starts

### MFE (Mel-Frequency Energy) tab:

   - Keep the High Frequency as 8000 as according to Nyquist theorem 16KHz/2 = 8000 Hz
   - Rest can be kept the same
   - Save parameters
   - Generate features

### Classifier tab:

   - We can enable Learned Optimizer and Data Augmentation if it struggles with real world but for our case it is not needed and reduces computation drastically.
   - The augmentation just gives varied example to make it more robust, so it is not necessarily better to turn it on.
   - Save and train

### Analysis:

   - Check the confusion table and explain
   - Say the Data explorer has different clouds for different label and also the errors occurs at boundary


