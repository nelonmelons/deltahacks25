#include <Servo.h>

Servo squirter; // First servo
Servo servo;    // Second servo

bool squirterActive = false; // Flag to control the squirter
bool sweeperActive = false;  // Flag to control the continuous sweeper

void setup() {
  Serial.begin(9600); // Start serial communication
  squirter.attach(4); // Attach the first servo to pin 4
  servo.attach(9);    // Attach the second servo to pin 9
  
  // Initialize servos to a neutral position
  squirter.write(0);
  servo.write(0);
}

void loop() {
  // Check if there's data from the serial interface
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming string
    command.trim(); // Remove any trailing whitespace

    if (command == "true") {
      squirterActive = true; // Activate squirter loop
    } else if (command == "toggle_sweeper") {
      sweeperActive = !sweeperActive; // Toggle the sweeper activity
    }
  }

  // Run squirter loop if active
  if (squirterActive) {
  for (int pos = 180; pos >= 0; pos -= 5) {  // Move quickly backwards (clockwise)
    squirter.write(pos); // Move to the current position
    delay(5);            // Small delay for faster motion
  }

  for (int pos = 0; pos <= 180; pos += 5) {  // Move quickly counterclockwise
    squirter.write(pos); // Move to the current position
    delay(5);            // Small delay for faster motion
  }

    squirterActive = false; // Reset flag
  }

  // Continuous sweeping for the second servo if active
  if (sweeperActive) {
    for (int angle = 0; angle <= 90; angle += 1) {
      servo.write(angle);
      delay(10);
    }
    for (int angle = 90; angle >= 0; angle -= 1) {
      servo.write(angle);
      delay(10);
    }
  }
}
