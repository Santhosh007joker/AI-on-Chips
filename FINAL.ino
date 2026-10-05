#include <driver/i2s.h>

#define I2S_WS   21
#define I2S_SCK  19
#define I2S_SD   18
#define I2S_PORT I2S_NUM_1
#define SAMPLE_RATE 16000
#define LED_PIN  2

void setup() {
  Serial.begin(921600);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

void loop() {
  if (Serial.available() && Serial.read() == 'r') {
    int16_t buffer[256];
    size_t bytesRead;
    bool recording = true;

    unsigned long lastBlink = 0;
    bool ledState = false;

    while (recording) {
      i2s_read(I2S_PORT, buffer, sizeof(buffer), &bytesRead, portMAX_DELAY);
      int count = bytesRead / sizeof(int16_t);

      for (int i = 0; i < count; i++) {
        int16_t sample16 = buffer[i] * 8;
        Serial.write((uint8_t*)&sample16, 2);
      }

      if (millis() - lastBlink > 200) {
        ledState = !ledState;
        digitalWrite(LED_PIN, ledState);
        lastBlink = millis();
      }

      if (Serial.available() && Serial.peek() == 's') {
        Serial.read();
        recording = false;
      }
    }

    digitalWrite(LED_PIN, LOW);
  }
}